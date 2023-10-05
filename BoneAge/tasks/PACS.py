import json
import traceback
from datetime import datetime, timedelta, time
from orthanc_api_client import OrthancApiClient
from orthanc_api_client.resources import Resources

from django.conf import settings
from django_q.models import Schedule
from django.apps import apps
from django.core.files.base import ContentFile

from BoneAge.models import PACS_QR, PACS_QR_Log
from BoneAge.apis.dicom import create_dcm
from BoneAge.apis.admin import allocate_task

def start(pacs_qr_id):
    pacs_qr = PACS_QR.objects.get(id=pacs_qr_id)
    schedule = Schedule.objects.create(
        name= pacs_qr.base_PACS.name + '|' +
            pacs_qr.name + '|' +
            datetime.today().strftime('%Y-%m-%d'),
        func='BoneAge.tasks.PACS.always_run',
        hook='BoneAge.tasks.PACS.clear_unmigrated',
        schedule_type=Schedule.MINUTES,
        minutes=pacs_qr.interval,
        repeats=-1,
    )
    schedule.args = str(pacs_qr.id) + ',' + str(schedule.id)
    schedule.save()

def always_run(pacs_qr_id, schedule_id):
    pacs_qr = PACS_QR.objects.get(id=pacs_qr_id)
    schedule = Schedule.objects.get(id=schedule_id)

    title = '【' + pacs_qr.name + '|' + str(schedule.id) + '|' + str(schedule.repeats) +'】'
    print(title + '开始于' + datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    print(title + '下次执行于' + schedule.next_run.strftime('%Y/%m/%d %H:%M:%S'))
    query_start_time = schedule.next_run - timedelta(minutes=pacs_qr.interval*3)
    query_end_time = query_start_time + timedelta(minutes=pacs_qr.interval)
    StudyDate = query_start_time.strftime('%Y%m%d')
    StudyTime = query_start_time.time().strftime('%H%M%S') + '-' + query_end_time.time().strftime('%H%M%S')
    query = json.loads(pacs_qr.query)
    query['StudyDate'] = StudyDate
    query['StudyTime'] = StudyTime
    if query_start_time.date() == query_end_time.date():
        retrieve(pacs_qr, schedule, query)
    else:
        StudyTime = query_start_time.time().strftime('%H%M%S') + '-' + '235959'
        query['StudyTime'] = StudyTime
        retrieve(pacs_qr, schedule, query)
        query['StudyDate'] = query_end_time.strftime('%Y%m%d')
        StudyTime = '000000' + '-' + query_end_time.time().strftime('%H%M%S')
        query['StudyTime'] = StudyTime
        retrieve(pacs_qr, schedule, query)

def retrieve(pacs_qr, schedule, query):
    title = '【' + pacs_qr.name + '|' + str(schedule.id) + '|' + str(schedule.repeats) +'】'
    StudyDate = query['StudyDate']
    StudyTime = query['StudyTime']
    print(title + 'StudyDuration:' + StudyDate + ' ' + StudyTime)
    print(title + 'C-MOVE开始于' + datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    orthanc = OrthancApiClient('http://localhost:' + str(settings.PACS_LOCAL['HttpPort']) + '/')
    remote_modality_alias = pacs_qr.base_PACS.name
    remote_studies = orthanc.modalities.query_studies(
        from_modality=remote_modality_alias,
        query=query
    )
    for index, study in enumerate(remote_studies):
        print(title + '获取序列：' + str(index + 1) + '/' + str(len(remote_studies)))
        orthanc.modalities.retrieve_study(from_modality='PACS',dicom_id=study.dicom_id)
    
    instances = []
    studies = orthanc.studies.find(query)
    for study in studies:
        for series in study.series:
            if series.main_dicom_tags.get('Modality') in ['DX']:
                for instance in series.instances:
                    instances.append(instance.orthanc_id)
            else:
                Resources(orthanc,'series/').delete(series.orthanc_id)
    print(title + 'C-MOVE完成于：' + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + '，共' + str(len(instances)) + '个影像文件')
    
    return PACS_QR_Log.objects.create(
        pacs_qr=pacs_qr,
        schedule=schedule,
        StudyDate=StudyDate,
        StudyTime=StudyTime,
        retrieved_instances='\n'.join(instances)
    )

# 解析后放入CQMU系统
def clear_unmigrated(task): 
    orthanc = OrthancApiClient('http://localhost:' + str(settings.PACS_LOCAL['HttpPort']) + '/')
    logs = PACS_QR_Log.objects.filter(migrated=False)
    if not logs: return None
    title = '【CQMU入库同步】'
    print(title + '开始于' + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + '，共' + str(len(logs)) + '条捕获记录需同步')
    log_id = ' '.join(str(log.id) for log in logs)
    print(title + '记录id：' + log_id)
    successed_count = 0
    for log in logs:
        pacs_qr = log.pacs_qr
        instance_ids = log.retrieved_instances.split('\n')
        new_dcms = migrate(orthanc, instance_ids, pacs_qr.allocate_to, pacs_qr.create_user.username)
        try:
            for dcm in new_dcms:
                if allocate_task(
                        dcm,
                        pacs_qr.create_user,
                        pacs_qr.standard,
                        pacs_qr.allocate_to,
                        pacs_qr.confidence / 100,
                        delete_with_source=True
                    ):
                    successed_count += 1
            try: orthanc.instances.delete(orthanc_ids=instance_ids)
            except: pass
        except Exception: traceback.print_exc()
        log.migrated = True
        log.save()
        
    print(title + '完成于' + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + '，成功同步' + str(successed_count) + '个手骨影像')

def migrate(orthanc, instance_ids, allocate_to, prefix):
    new_dcms = []
    for orthanc_id in instance_ids:
        try:
            dcm_bytes = orthanc.instances.get_file(orthanc_id)
            new_dcm, error = create_dcm(
                ContentFile(dcm_bytes, orthanc_id + '.dcm'),
                allocate_to,
                prefix
            )
            if not new_dcm: continue
            new_dcms.append(new_dcm)
        except Exception:
            traceback.print_exc()
            continue
    return new_dcms

# TODO: 带休息时间的启动。暂时不考虑。注意跨天问题。
# 带休息时间的每日启动（PACS配置了启动时间、关闭时间）
# def daily_repeat(pacs_qr_id):
#     pacs_qr = PACS_QR.objects.get(id=pacs_qr_id)
#     start_datetime = datetime.combine(datetime.today(), pacs_qr.start_time)
#     end_datetime = datetime.combine(datetime.today(), pacs_qr.end_time)
#     repeats = math.ceil((end_datetime - start_datetime).total_seconds() / 60 / pacs_qr.interval)
#     schedule = Schedule.objects.create(
#         name= pacs_qr.base_PACS.name + '|' +
#             pacs_qr.name + '|' +
#             datetime.today().strftime('%Y-%m-%d'),
#         func='BoneAge.tasks.PACS.retrieve',
#         hook='BoneAge.tasks.PACS.migrate_to_CQMU',
#         schedule_type=Schedule.MINUTES,
#         minutes=pacs_qr.interval,
#         repeats=repeats + 2,
#         next_run = start_datetime
#     )
#     schedule.args = str(schedule.id) + ',' + str(pacs_qr.id) + ',' + '0'
#     schedule.save()

# 影像获取至Orthanc
# 注：每一个时间点抓取上一个interval的影像，以留出影像进入远程pacs的时间。第0、1轮不执行操作
# def retrieve(schedule_id, pacs_qr_id, repeats_done):
#     if repeats_done == 0 or repeats_done == 1: 
#         return 0
#     orthanc = OrthancApiClient('http://localhost:' + str(settings.PACS_LOCAL['HttpPort']) + '/')
    
#     pacs_qr = PACS_QR.objects.get(id=pacs_qr_id)
#     StudyDate = datetime.today().strftime('%Y%m%d')
#     start_time= pacs_qr.start_time
#     expired_minutes = (repeats_done - 2) * pacs_qr.interval
#     # TODO: interval大于10分钟的给它切成臊子每个单独开任务（比如每小时同步一次，按每10分钟切段）
#     StudyTime_start = datetime.combine(datetime.today(), start_time) + timedelta(minutes=expired_minutes)
#     StudyTime_end = StudyTime_start + timedelta(minutes=pacs_qr.interval)
#     StudyTime = StudyTime_start.time().strftime('%H%M%S') + '-' + StudyTime_end.time().strftime('%H%M%S')
#     remote_modality_alias = pacs_qr.base_PACS.name
#     query = json.loads(pacs_qr.query)
#     query['StudyDate'] = StudyDate
#     query['StudyTime'] = StudyTime
#     title = '[' + str(pacs_qr.name) + '|' + StudyDate + '|' + str(repeats_done) + ']'
#     print('————————任务开始' + datetime.now().strftime('%m/%d/%H:%M:%S') + '————————')
#     print(title + '影像抓取目标时间段：' + StudyDate + ' ' + StudyTime)
#     remote_studies = orthanc.modalities.query_studies(
#         from_modality=remote_modality_alias,
#         query=query
#     )
#     print(title + '查询完成：' + datetime.now().strftime('%m/%d/%H:%M:%S'))
#     for study in remote_studies: orthanc.modalities.retrieve_study(from_modality='PACS',dicom_id=study.dicom_id)
#     print(title + '抓取完成：' + datetime.now().strftime('%m/%d/%H:%M:%S'))

#     instances = []
#     studies = orthanc.studies.find(query)
#     for study in studies:
#         for series in study.series:
#             if series.main_dicom_tags.get('Modality') in ['DX']:
#                 for instance in series.instances:
#                     instances.append(instance)
#             else:
#                 Resources(orthanc,'series/').delete(series.orthanc_id)
#     # create pacs log, instance related infos
#     print('- - - - - - - - 抓取结果- - - - - - - -')
#     for instance in instances: print(instance.orthanc_id)
#     print('- - - - - - - - 抓取结束，开始入库' + datetime.now().strftime('%m/%d/%H:%M:%S') + '- - - - - - - -')

#     schedule = Schedule.objects.get(id=schedule_id)
#     arguments = schedule.args.split(',')
#     # schedule repeat增加一轮
#     arguments[-1] = str(int(arguments[-1]) + 1)
#     schedule.args = ','.join(arguments)
#     schedule.save()

