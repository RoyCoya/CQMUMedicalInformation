from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth import get_user_model

from BoneAge.models import DicomFile
from BoneAge.apis.admin import allocate_task

class Command(BaseCommand):
    help = r"手动分配指定任务至用户"

    def add_arguments(self, parser):
        parser.add_argument("--id", nargs="+", type=int, help='BoneAge dcm ID')
        parser.add_argument("--from", type=str, default='CQMU', help='The user who allocate tasks')
        parser.add_argument("--to", type=str, default='test1', help='Allocated to whom')
        parser.add_argument("--standard", choices=['CHN', 'RUS'] , default='CHN', type=str, help='CHN or RUS')
        parser.add_argument("-C", "--confidence", type=float, default=0.8, help='BoneAge dcm ID')

    def handle(self, *args, **options):
        confidence = options['confidence']
        if not 0<= confidence <=1: raise CommandError('confidence should be between 0 and 1')

        id = options['id']
        dcm_to_allocate = DicomFile.objects.filter(id__in=id)
        allocator = get_user_model().objects.get(username=options['from'])
        allocate_to = get_user_model().objects.get(username=options['to'])
        standard = options['standard']
        for dcm in dcm_to_allocate:
            if allocate_task(
                dcm=dcm,
                allocator=allocator,
                allocate_standard=standard,
                allocated_to=allocate_to,
                confidence=confidence
            ): self.stdout.write(self.style.SUCCESS('任务%d分配至%s' % (dcm.id, allocate_to.username)))
