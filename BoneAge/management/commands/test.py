from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "测试用"

    # def add_arguments(self, parser):
    #     parser.add_argument("pacs_qr_id", nargs="+", type=int)

    def handle(self, *args, **options):
        # print(test('CHN', 'Female'))
        pass