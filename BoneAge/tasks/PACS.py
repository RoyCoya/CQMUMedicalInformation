import json
import math
from datetime import datetime, timedelta, time
from pyorthanc import find, Orthanc, RemoteModality

from django.conf import settings
from django_q.models import Schedule

from BoneAge.models import PACS_QR

# 每日启动
def DailyRepeat(pacs_qr_id):
    pacs_qr = PACS_QR.objects.get(id=pacs_qr_id)
    start_datetime = datetime.combine(datetime.today(), pacs_qr.start_time)
    end_datetime = datetime.combine(datetime.today(), pacs_qr.end_time)
    repeats = (end_datetime - start_datetime).total_seconds() / 60 / pacs_qr.interval
    Schedule.objects.create(
        name= pacs_qr.base_PACS.name + '|' +
            pacs_qr.name + '|' +
            datetime.today().strftime('%Y-%m-%d'),
        func='BoneAge.tasks.PACS.Retrieve',
        hook='BoneAge.tasks.PACS.RetireveEnd',
        schedule_type=Schedule.MINUTES,
        minutes=pacs_qr.interval,
        repeats=math.ceil(repeats),
        args='4,5',
        next_run = datetime.combine(datetime.today(), time(6, 0))
    )

# 影像获取
def Retrieve(a,b):
    print(a+b)
    # orthanc = Orthanc(url='http://localhost:' + settings.PACS_local['HttpPort'] + '/')
    # for remote_pacs in PACS_QR.objects.all():
    #     remote_modality = RemoteModality(Orthanc(orthanc, remote_pacs.base_PACS.name))
    #     query = json.loads(remote_pacs.query)
    #     query_response = remote_modality.query(data=query)
    #     remote_modality.move(query_response['QUERY_ID'], settings.PACS_local['DicomAet'])

# 获取结束
def RetireveEnd():
    print('Retrive Finished')