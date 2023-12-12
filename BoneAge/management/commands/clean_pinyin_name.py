import os

from django.conf import settings
from django.core.management.base import BaseCommand

from PatientManagement.models import Patient

class Command(BaseCommand):
    help = r"根据已有的 {患者ID:中文名} 的txt文件刷新系统内的患者名"
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('中文名更新开始'))
        patients_chinese_name_dic = {}
        with open(
            os.path.join(settings.BASE_DIR, 'doc/references/patients.txt'),
            encoding="utf-8"
        ) as patients:
            for patient in patients:
                details = patient.split('\t')
                patient_id = details[0]
                name = details[1]
                patients_chinese_name_dic[patient_id] = name
        patients = Patient.objects.all()
        count = 0
        for patient in patients:
            id = patient.Patient_ID
            try: 
                name = patients_chinese_name_dic[id].replace('\n','')
                patient.name = name
                patient.save()
                count += 1
            except Exception as e: print(e)
        self.stdout.write(self.style.SUCCESS('中文名更新成功，共更新%s条记录' % count))