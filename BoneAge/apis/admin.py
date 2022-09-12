import os
import cv2
import numpy as np
from datetime import datetime
from pydicom.filereader import dcmread

from django.shortcuts import redirect
from django.http import *
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files import File
from django.urls import reverse

from BoneAge.apis.public_func import login_check
from BoneAge.yolo.yolo_onnx import YOLOV5_ONNX
from BoneAge.object_swinT.BoneGrade import BoneGrade

from DICOMManagement.models import DicomFile as base_DicomFile
from PatientManagement.models import Patient as base_Patient
from BoneAge.models import BoneDetail, DicomFile, Task

# dcm图像像素压缩到255
def normalize(img_normalize, number):
    high = np.max(img_normalize)
    low = np.min(img_normalize)
    img_normalize = (img_normalize - low) / (high - low)
    img_normalize = (img_normalize * number).astype('uint8')
    return img_normalize

# 上传dcm
def api_upload_dcm(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权上传dcm文件")
    # 错误列表改成[{name:'', error:''}]形式
    broken_files = []
    sop_uid_miss_files = []
    duplicate_files = []
    
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
        # TODO: 这里的new_file.dcm为啥没写成new_file.dcm.path？有时间了试试
        try: reader = dcmread(new_file.dcm, force=True)
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
            sop_uid_miss_files.append(file.name)
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

        #创建dcm对应的task实例、对应的骨骼
        task = Task.objects.create(dcm_file=BoneAge_new_file, modify_user=user)
        BoneDetail.objects.create(task=task, name='Radius', modify_user=user)
        BoneDetail.objects.create(task=task, name='Ulna', modify_user=user)
        BoneDetail.objects.create(task=task, name='First Metacarpal', modify_user=user)
        BoneDetail.objects.create(task=task, name='Third Metacarpal', modify_user=user)
        BoneDetail.objects.create(task=task, name='Fifth Metacarpal', modify_user=user)
        BoneDetail.objects.create(task=task, name='First Proximal Phalange', modify_user=user)
        BoneDetail.objects.create(task=task, name='Third Proximal Phalange', modify_user=user)
        BoneDetail.objects.create(task=task, name='Fifth Proximal Phalange', modify_user=user)
        BoneDetail.objects.create(task=task, name='Third Middle Phalange', modify_user=user)
        BoneDetail.objects.create(task=task, name='Fifth Middle Phalange', modify_user=user)
        BoneDetail.objects.create(task=task, name='First Distal Phalange', modify_user=user)
        BoneDetail.objects.create(task=task, name='Third Distal Phalange', modify_user=user)
        BoneDetail.objects.create(task=task, name='Fifth Distal Phalange', modify_user=user)

    print('无法读取的dcm：',broken_files)
    print('SOP UID 缺失：',sop_uid_miss_files)
    print('重复的dcm：',duplicate_files)

    # TODO:操作成功后单独弹出页面提示上传失败的、成功的、重复的各个文件
    return HttpResponseRedirect(reverse('BoneAge_index',args=(1,0,0)))

# 解析数据库中未初始化（转png、骨骼定位）的dcm
def api_analyze_dcm(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权解析dcm文件")

    dcms_to_analyze = DicomFile.objects.filter(error=202)
    object_path = str(settings.STATICFILES_DIRS[0]) + '/yolo_model/yolo_roi.onnx'
    object_model = YOLOV5_ONNX(object_path)
    grade_path = str(settings.STATICFILES_DIRS[0]) + '/swinT_weights'
    grade_model =  BoneGrade(grade_path, 224)
    for BoneAge_dcm in dcms_to_analyze:
        dcm = BoneAge_dcm.base_dcm
        # 转png
        try:
            reader = dcmread(dcm.dcm, force=True)
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
            # TODO:检查是否为手骨图
        except Exception as e:
            print(e)
            BoneAge_dcm.error = 415
            BoneAge_dcm.save()
            continue
        dcm.save()
        
        # 目标检测，录入骨骼位置
        bones = BoneDetail.objects.filter(task__dcm_file=BoneAge_dcm)
        # 所有骨骼初始化为404
        for bone in bones:
            bone.error = 404
            bone.save()
        bone_detected = object_model.infer(img_array)
        # 组装骨骼位置信息
        for name,position in bone_detected.items():
            try: 
                position = position[1]
                bone = bones.get(name=name)
                bone.center_x = position[0]
                bone.center_y = position[1]
                bone.width = position[2]
                bone.height = position[3]
                bone.error = 0
                bone.save()
            except Exception as e:
                print(e)
                pass
        # 组装骨龄评级信息
        for name,position in bone_detected.items():
            try: 
                position = position[0]
                img_crop = img_array[int(position[1]):int(position[3]), int(position[0]):int(position[2])]
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                r, g, b = cv2.split(img_crop)
                r1 = clahe.apply(r)
                g1 = clahe.apply(g)
                b1 = clahe.apply(b)
                img_crop = cv2.merge([r1, g1, b1])
                img_crop = normalize(img_crop, 255)
                level = grade_model.pre_gray(img_crop, name)
                bone = bones.get(name=name)
                bone.level = level
                bone.save()
            except Exception as e:
                print(e)
                pass
        BoneAge_dcm.error = 0
        BoneAge_dcm.save()
        
    return HttpResponseRedirect(reverse('BoneAge_index',args=(1,0,0)))

# 分配指定数量的任务给指定用户
def api_allocate_tasks(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权分配任务")

    user_model = get_user_model()
    user = user_model.objects.get(id=request.POST['allocate_to'])
    tasks = Task.objects.filter(dcm_file__error=0).filter(closed=False).filter(allocated_to=None)
    tasks_to_allocate_count = request.POST['tasks_to_allocate_count']
    for task in tasks[0:int(tasks_to_allocate_count)]:
        task.allocated_to = user
        task.allocated_datetime = datetime.now()
        task.save()
    return HttpResponseRedirect(reverse('BoneAge_index',args=(1,0,0)))

# 平均分配任务给所有用户
def api_allocate_tasks_random(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权分配任务")
    
    user_model = get_user_model()
    users = user_model.objects.filter(is_active=True).exclude(is_staff=True)
    users_amount = users.count()
    tasks = Task.objects.filter(dcm_file__error=0).filter(closed=False).filter(allocated_to=None)
    tasks_amount = tasks.count()
    step = int(tasks_amount / users_amount)
    i = 0
    for user in users:
        tasks_for_user = tasks[i:(i+step)]
        for task in tasks_for_user:
            task.allocated_to = user
            task.allocated_datetime = datetime.now()
            task.save()
    return HttpResponseRedirect(reverse('BoneAge_index',args=(1,0,0)))
    