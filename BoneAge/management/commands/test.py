from django.core.management.base import BaseCommand
from DICOMManagement.models import DicomFile

class Command(BaseCommand):
    help = "测试用"

    def handle(self, *args, **options):
        dcms = DicomFile.objects.all()
        for dcm in dcms:
            if dcm.Study_Date and dcm.patient.birthday:
                dcm.study_age = round((dcm.Study_Date - dcm.patient.birthday).days / 365, 2)
                dcm.save()
        pass