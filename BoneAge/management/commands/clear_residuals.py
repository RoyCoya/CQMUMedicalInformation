import os
from tqdm import tqdm
from orthanc_api_client import OrthancApiClient

from django.core.management.base import BaseCommand
from django.conf import settings

from DICOMManagement.models import DicomFile

def delete_dcm(relative_path, file_path):
    try:
        DicomFile.objects.get(dcm=relative_path)
    except:
        os.remove(file_path)
        print('deleted ' + relative_path)

def delete_png(relative_path, file_path):
    try:
        DicomFile.objects.get(dcm_to_image=relative_path)
    except:
        os.remove(file_path)
        print('deleted ' + relative_path)

class Command(BaseCommand):
    help = "清理开发过程中留下的冗余dicom文件（没被数据库记录的）"

    def handle(self, *args, **options):
        root_dir = 'D:/CQMUMedicalInformation/userfile'
        orthanc = OrthancApiClient('http://localhost:' + str(settings.PACS_LOCAL['HttpPort']) + '/')
        orthanc.patients.delete_all()

        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in tqdm(filenames):
                file_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(file_path, root_dir)
                relative_path = os.path.normpath(relative_path).replace('\\', '/')
                if filename.endswith('.dcm'): delete_dcm(relative_path, file_path)
                if filename.endswith('.png'): delete_png(relative_path, file_path)
