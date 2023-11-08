# import math
# from datetime import datetime, time, timedelta

# from django_q.models import Schedule
# from django.core.management.base import BaseCommand

# from BoneAge.models import PACS_QR

# class Command(BaseCommand):
#     help = "手动启动PACS_QR，带启动/停止时间，参数：pacs_id"

#     def add_arguments(self, parser):
#         parser.add_argument("pacs_qr_id", nargs="+", type=int)

#     def handle(self, *args, **options):
#         for id in options["pacs_qr_id"]:
#             pacs_qr = PACS_QR.objects.get(id=id)
#             today_start_datetime = datetime.combine(datetime.today(), pacs_qr.start_time)
#             today_end_datetime = datetime.combine(datetime.today(), pacs_qr.end_time)
#             next_run= today_start_datetime
#             if datetime.now() > today_start_datetime: next_run = today_start_datetime + timedelta(days=1)
#             Schedule.objects.create(
#                 name= '[启动]' + '骨龄' + '|' +
#                     pacs_qr.name +'|' +
#                     datetime.today().strftime('%Y-%m-%d'),
#                 args=str(id),
#                 func='BoneAge.tasks.PACS.daily_repeat',
#                 schedule_type=Schedule.DAILY,
#                 next_run= next_run
#             )
#             if datetime.now() > today_start_datetime and datetime.now() < today_end_datetime:
#                 print('today reduction')
#                 start_datetime = datetime.now() + timedelta(minutes=pacs_qr.interval)
#                 end_datetime = datetime.combine(datetime.today(), pacs_qr.end_time)
#                 repeats = (end_datetime - start_datetime).total_seconds() / 60 / pacs_qr.interval
#                 schedule = Schedule.objects.create(
#                     name= pacs_qr.base_PACS.name + '|' +
#                         pacs_qr.name + '|' +
#                         datetime.today().strftime('%Y-%m-%d'),
#                     func='BoneAge.tasks.PACS.retrieve',
#                     hook='BoneAge.tasks.PACS.migrate_to_CQMU',
#                     schedule_type=Schedule.MINUTES,
#                     minutes=pacs_qr.interval,
#                     repeats=math.ceil(repeats) + 1,
#                     next_run=start_datetime,
#                 )
#                 repeats_done = (start_datetime - today_start_datetime).total_seconds() / 60 / pacs_qr.interval
#                 schedule.args = str(schedule.id) + ',' + str(pacs_qr.id) + ',' + str(int(repeats_done))
#                 schedule.save()