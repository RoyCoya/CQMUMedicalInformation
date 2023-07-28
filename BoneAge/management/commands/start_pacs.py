import math
from datetime import datetime, time, timedelta

from django_q.models import Schedule
from django.core.management.base import BaseCommand

from BoneAge.tasks.PACS import Retrieve
from BoneAge.models import PACS_QR

class Command(BaseCommand):
    help = "手动启动PACS_QR，参数：pacs_id"

    def add_arguments(self, parser):
        parser.add_argument("pacs_qr_id", nargs="+", type=int)

    def handle(self, *args, **options):
        for id in options["pacs_qr_id"]:
            pacs_qr = PACS_QR.objects.get(id=id)
            Schedule.objects.create(
                name= '[启动]' + '骨龄' + '|' +
                    pacs_qr.name +'|' +
                    datetime.today().strftime('%Y-%m-%d'),
                args=str(id),
                func='BoneAge.tasks.PACS.DailyRepeat',
                schedule_type=Schedule.DAILY,
                next_run=datetime.combine(datetime.today(), pacs_qr.start_time) + timedelta(days=1)
            )
            # 如果启动时间已经超过设定的每日启动时间，则补充一份当日的once任务
            if datetime.now() > datetime.combine(datetime.today(), pacs_qr.start_time):
                start_datetime = datetime.now() + timedelta(minutes=pacs_qr.interval)
                end_datetime = datetime.combine(datetime.today(), pacs_qr.end_time)
                repeats = (end_datetime - start_datetime).total_seconds() / 60 / pacs_qr.interval
                Schedule.objects.create(
                    name= '骨龄' + '|' +
                        pacs_qr.name + '|' +
                        datetime.today().strftime('%Y-%m-%d'),
                    func='BoneAge.tasks.PACS.Retrieve',
                    hook='BoneAge.tasks.PACS.RetireveEnd',
                    schedule_type=Schedule.MINUTES,
                    minutes=pacs_qr.interval,
                    repeats=math.ceil(repeats),
                    args='4,5',
                    next_run=start_datetime,
                )