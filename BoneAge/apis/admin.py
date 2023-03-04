import os
from datetime import datetime

import cv2
import numpy as np
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.http import *
from django.shortcuts import redirect, render
from pydicom.filereader import dcmread

import BoneAge.apis.standard as bone_standars

from BoneAge.apis.public_func import login_check
from BoneAge.apis.bone_analysis import bone_detect
from BoneAge.models import BoneDetail, DicomFile, Task
from DICOMManagement.models import DicomFile as base_DicomFile
from PatientManagement.models import Patient as base_Patient

''' dcm图像像素压缩到255 '''
def normalize(img_normalize, number):
    high = np.max(img_normalize)
    low = np.min(img_normalize)
    img_normalize = (img_normalize - low) / (high - low)
    img_normalize = (img_normalize * number).astype('uint8')
    return img_normalize

# 上传dcm，转png入库
def api_upload_dcm(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权上传dcm文件")
    # TODO:错误列表改成[{name:'', error:''}]形式
    success_files = []
    broken_files = []
    duplicate_files = []
    not_hand_files = []
    img_convert_failed_files = []
    
    # 上传
    for file in request.FILES.getlist('dcm_files'):
        suffix = file.name.split('.')[-1]
        if suffix != 'dcm' and suffix != 'DCM' : continue
        file.name = 'upload_' + file.name.lower()
        new_file = base_DicomFile.objects.create(
            dcm=File(file),
            create_user=user,
            modify_user=user,
        )

        # 检验dcm能否读取（reader是否可以启动）
        try: reader = dcmread(new_file.dcm.path, force=True)
        except Exception as e:
            print(e)
            try: os.remove(new_file.dcm.path)
            except: pass
            new_file.delete()
            broken_files.append(file.name)
            continue
        
        # 检验dcm能否读取sop_instance_uid
        sop_instance_uid = None
        try: sop_instance_uid = reader.SOPInstanceUID
        except Exception as e:
            print(e)
            try: os.remove(new_file.dcm.path)
            except: pass
            new_file.delete()
            broken_files.append(file.name)
            continue
        # 以sop instance uid验证dicom是否重复
        if sop_instance_uid:
            if base_DicomFile.objects.filter(SOP_Instance_UID=sop_instance_uid):
                try: os.remove(new_file.dcm.path)
                except: pass
                new_file.delete()
                duplicate_files.append(file.name)
                continue
        new_file.SOP_Instance_UID = sop_instance_uid
        # 挂载患者或创建新患者并挂载dcm
        patient = base_Patient.objects.filter(Patient_ID=reader.PatientID)
        if(patient): 
            new_file.patient = patient[0]
        else:
            name = None
            Patient_ID = None
            sex = None
            birthday = None
            
            try: name = reader.PatientName
            except Exception as e:
                print(e)
                try: os.remove(new_file.dcm.path)
                except: pass
                new_file.delete()
                broken_files.append(file.name)
                continue
            try: Patient_ID = reader.PatientID
            except Exception as e:
                print(e)
                try: os.remove(new_file.dcm.path)
                except: pass
                new_file.delete()
                broken_files.append(file.name)
                continue
            try: sex = 'Male' if reader.PatientSex == 'M' else 'Female'
            except Exception as e:
                print(e)
                try: os.remove(new_file.dcm.path)
                except: pass
                new_file.delete()
                broken_files.append(file.name)
                continue
            try: birthday = datetime.strptime(reader.PatientBirthDate,'%Y%m%d').date()
            except Exception as e:
                print(e)
                try: os.remove(new_file.dcm.path)
                except: pass
                new_file.delete()
                broken_files.append(file.name)
                continue
            patient = base_Patient.objects.create(
                name=name,
                Patient_ID=Patient_ID,
                sex=sex,
                birthday=birthday,
                modify_user=user,
            )
            new_file.patient = patient
        # 扩展信息
        study_date = None
        try: study_date = datetime.strptime(reader.StudyDate,'%Y%m%d').date()
        except Exception as e: print(e)
        new_file.Study_Date = study_date
        # 结束dcm校验，保存。创建BoneAge专用DicomFile实例
        new_file.save()
        BoneAge_new_file = DicomFile.objects.create(
            base_dcm = new_file,
            error = 202,
            create_user = user,
            modify_user = user,
        )
        dcm = BoneAge_new_file.base_dcm

        # TODO: 检查是否为手骨
        # try:
        # except Exception as e:
        #     print(e)
        #     BoneAge_new_file.error = 403
        #     BoneAge_new_file.save()
        #     not_hand_files.append(file.name)

        # 转png
        try:
            reader = dcmread(dcm.dcm.path, force=True)
            img_array = reader.pixel_array
            img_array = cv2.GaussianBlur(img_array, (5, 5), sigmaX=0, sigmaY=0)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            img_array = clahe.apply(img_array)
            img_array = normalize(img_array, 255)
            img = img_array.squeeze()
            img = np.expand_dims(img, axis=2)
            img_array = np.concatenate((img, img, img), axis=-1)
            cv2.imwrite(settings.MEDIA_ROOT+dcm.dcm.name + ".png", img_array, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
            dcm.dcm_to_image = dcm.dcm.name + ".png"
            dcm.save()
        except Exception as e:
            print(e)
            BoneAge_new_file.error = 415
            BoneAge_new_file.save()
            img_convert_failed_files.append(file.name)
            continue
        BoneAge_new_file.error = 0
        BoneAge_new_file.save()

        success_files.append(file.name)
    
    context = {
        'success_files' : success_files,
        'broken_files' : broken_files,
        'duplicate_files' : duplicate_files,
        'not_hand_files' : not_hand_files,
        'img_convert_failed_files' : img_convert_failed_files,
    }
    return render(request, 'BoneAge/index/admin/upload_results.html', context)

# 任务分配
# 选择error为0的骨龄DicomFile、创建Task并确认所使用的标准，用对应模型识别骨骼位置、骨龄，添加BoneDetails
def api_allocate_tasks(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权分配任务")

    dcms_to_allocate_ids = str(request.POST['dcms_id']).split(' ')[0:-1]
    for i in range(len(dcms_to_allocate_ids)):  dcms_to_allocate_ids[i] = int(dcms_to_allocate_ids[i])
    dcms_to_allocate = DicomFile.objects.filter(id__in=dcms_to_allocate_ids)
    allocate_standard = request.POST['allocate_standard']
    allocated_to = get_user_model().objects.get(id=request.POST['allocated_to'])
    
    # 当前提交的dcm状态改为“分配中”，使这些dcm在分配界面隐藏
    for dcm in dcms_to_allocate:
        dcm.error = 102
        dcm.save()

    # 分配dcm。该步骤会持续一段时间
    for dcm in dcms_to_allocate:
        # 如果当前需要创建的任务已存在（异步时可能有冲突），则跳过
        if Task.objects.filter(dcm_file=dcm).filter(standard=allocate_standard): continue

        # 创建任务
        new_task = Task.objects.create(
            dcm_file = dcm,
            standard = allocate_standard,
            allocated_to = allocated_to,
            allocated_datetime = datetime.now(),
            modify_user = user
        )
        
        # 创建骨骼信息
        bones_name = {
            'RUS' : lambda : bone_standars.RUS_CHN,
            'CHN' : lambda : bone_standars.CHN,
        }[new_task.standard]()
        for bone_name in bones_name: BoneDetail.objects.create(
            task=new_task, name=bone_name, modify_user=user, error=404
        )
        
        bone_detected = bone_detect(dcm.base_dcm.dcm_to_image.path, allocate_standard)
        bones = BoneDetail.objects.filter(task=new_task)

        for name, details in bone_detected.items():
            try: 
                bone = bones.get(name=name)
                bone.center_x = details['box'][0]
                bone.center_y = details['box'][1]
                bone.width = details['box'][2]
                bone.height = details['box'][3]
                bone.assessment = int(details['level'])
                bone.error = 0
                bone.save()
            except: pass

        dcm.error = 0
        dcm.save()

    return HttpResponse('任务分配成功')