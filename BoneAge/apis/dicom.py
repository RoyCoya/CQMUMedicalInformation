import cv2
import os
import numpy as np
from typing import Tuple, List, Dict, Any
from pydicom.filereader import dcmread
from pydicom.multival import MultiValue
from datetime import datetime

from django.conf import settings
from django.core.files import File

from DICOMManagement.models import DicomFile as base_DicomFile
from PatientManagement.models import Patient as base_Patient
from BoneAge.models import DicomFile

# TODO: 再解耦一次，输入为base_DicomFile的应该换成dcm reader的返回值或image bytes
def create_dcm(file, user, prefix)  -> Tuple[DicomFile, int]:
    suffix = file.name.split('.')[-1]
    if suffix != 'dcm' and suffix != 'DCM' : return None, 415
    file.name = prefix + '_' + user.username + '_' + file.name.lower()

    # 创建base dicom
    base_dcm, error = create_base_dcm(file, user)
    if not base_dcm: return None, error
    
    # 创建骨龄用的含扩展信息的DicomFile
    return DicomFile.objects.create(
        base_dcm = base_dcm,
        error = 0,
        create_user = user,
        modify_user = user,
    ), 0

def create_base_dcm(file : File, user) -> Tuple[base_DicomFile, int]:
    new_dcm = base_DicomFile.objects.create(
        dcm=File(file),
        create_user=user,
        modify_user=user,
    )

    # 基础信息
    try:
        required_tags = [
            'SOPInstanceUID',
            'PatientID',
            'PatientName',
            'PatientID', 
            'PatientSex', 
            'PatientBirthDate',
        ]
        tags = tags_check(new_dcm, required_tags, 'delete')
        if None in tags.values(): return None, 400
        if base_DicomFile.objects.filter(SOP_Instance_UID=tags['SOPInstanceUID']):
            delete_base_dcm(new_dcm)
            return None, 409
    except Exception as e:
        print(e)
        delete_base_dcm(new_dcm)
        return None, 400
        
    new_dcm.SOP_Instance_UID = tags['SOPInstanceUID']
    new_dcm.patient = get_dcm_patient(tags, user)
    
    # 扩展信息
    optional_tags = [
        'StudyDate',
        'WindowCenter',
        'WindowWidth',
    ]
    tags = tags_check(new_dcm, optional_tags, 'ignore')
    new_dcm.Study_Date = datetime.strptime(tags['StudyDate'],'%Y%m%d').date() if tags['StudyDate'] else None
    new_dcm.Window_Center = tags['WindowCenter']
    new_dcm.Window_Width = tags['WindowWidth']

    # 影像转换校验
    error = image_convert_check(new_dcm)
    if error: return None, error

    new_dcm.save()
    return new_dcm, 0

def delete_base_dcm(file : base_DicomFile):
    try:
        os.remove(file.dcm.path)
        os.remove(file.dcm_to_image.path)
    except Exception as e: print(e)
    file.delete()

def tags_check(file : base_DicomFile, tags_to_check : List[str], handler : str) -> Dict[str, Any]:
    """

    Check Dicom tags in given list.
    
    Parameters
    ----------
    file: DICOMManagement.modle.DicomFile
        BoneAge dicom file's base dicom file in DICOMManagement
    tags_to_check: list
        tags' name in dicom file, see in dicom standard
    handler: str
        ways to handle dicom file with missing or error tags. Choice: `delete` or `ignore`
    
    Returns
    -------
    tags: dict
        `{tag name : tag content}`, tag content is `None` when tag is error or missing
    """

    reader = dcmread(file.dcm.path, force=True)
    tags = {}

    for tag_name in tags_to_check:
        if hasattr(reader, tag_name): tags[tag_name] = getattr(reader, tag_name)
        else:
            {
                'delete' : lambda : delete_base_dcm(file),
                'ignore' : lambda : None,
            }[handler]()
            tags[tag_name] = None
        
    return tags

def image_convert_check(file : base_DicomFile) -> str:
    try:
        tags = tags_check(
            file,
            ['pixel_array','WindowCenter','WindowWidth'],
            'ignore'
        )
        img_array, window_center, window_width = tags['pixel_array'], tags['WindowCenter'], tags['WindowWidth']
        if img_array is None: return 204

        if window_center and window_width: img_array = window_image(img_array, window_center, window_width, 256)
        else: img_array = normalize(img_array, 255)
        img = img_array.squeeze()
        img = np.expand_dims(img, axis=2)
        img_array = np.concatenate((img, img, img), axis=-1)

        # 图像存至dcm同目录下
        cv2.imwrite(settings.MEDIA_ROOT+file.dcm.name + ".png", img_array, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        file.dcm_to_image = file.dcm.name + ".png"
        file.save()
    except Exception as e:
        print(e)
        delete_base_dcm(file)
        return 422

def get_dcm_patient(tags : dict, user) -> base_Patient:
    patient_log = base_Patient.objects.filter(Patient_ID=tags['PatientID'])
    if patient_log.exists(): return patient_log[0]
    else: return base_Patient.objects.create(
        name=tags['PatientName'],
        Patient_ID=tags['PatientID'],
        sex={
            'M' : 'Male',
            'F' : 'Female',
            'O' : 'Other'
        }[tags['PatientSex']](),
        birthday=datetime.strptime(tags['PatientBirthDate'],'%Y%m%d').date(),
        modify_user=user,
    )

def window_image(img_array, WindowCenter, WindowWidth, color_width):
    window_center = WindowCenter[0] if type(WindowCenter) == MultiValue else WindowCenter
    window_width = WindowWidth[0] if type(WindowWidth) == MultiValue else WindowWidth
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    img_array = np.clip(img_array, img_min, img_max)
    img_array = color_width/window_width*img_array + (window_width/2-window_center)*color_width/window_width
    return img_array

def normalize(img_normalize, number):
    high = np.max(img_normalize)
    low = np.min(img_normalize)
    img_normalize = (img_normalize - low) / (high - low)
    img_normalize = (img_normalize * number).astype('uint8')
    return img_normalize