import math
from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand

import BoneAge.tasks.PACS as PACS

class Command(BaseCommand):
    help = "手动启动PACS_QR，参数：pacs_id"

    def add_arguments(self, parser):
        parser.add_argument("pacs_qr_id", nargs="+", type=int)

    def handle(self, *args, **options):
        for id in options["pacs_qr_id"]:
            PACS.start(id)