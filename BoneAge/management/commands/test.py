from django.core.management.base import BaseCommand
from BoneAge.models import Task

class Command(BaseCommand):
    help = "测试用"

    def handle(self, *args, **options):
        finished_tasks = Task.objects.filter(closed=True)
        finished_tasks.update(status='finished')
        pass