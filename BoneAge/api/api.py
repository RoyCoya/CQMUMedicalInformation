import cv2
import os
import numpy as np
from datetime import date, datetime
from pydicom.filereader import dcmread
from shutil import copyfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import *
from django.urls import reverse
from django.core.files import File

from BoneAge.yolo.yolo_onnx import YOLOV5_ONNX
from BoneAge.models import *
from BoneAge.object_swinT.BoneGrade import BoneGrade

'''通用方法'''
# 登录检查
def login_check(request):
    user = request.user
    if not user.is_authenticated : return True
    else : return False

# 加载用户偏好设置
def load_preference(request):
    user = request.user
    preference = None
    try: preference = Preference.objects.get(user=user)
    except: preference = Preference.objects.create(user=user)
    return preference

# dcm图像像素压缩到255
def normalize(img_normalize, number):
    high = np.max(img_normalize)
    low = np.min(img_normalize)
    img_normalize = (img_normalize - low) / (high - low)
    img_normalize = (img_normalize * number).astype('uint8')
    return img_normalize

'''特定接口'''
# 切换快捷键开启状态
def api_preference_switch_shortcut(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    preference = Preference.objects.get(user=user)
    
    preference.shortcut = request.POST['shortcut'].title()
    preference.save()

    return HttpResponse("切换快捷键开启状态成功")

# 切换进入评分器时的默认骨骼
def api_preference_switch_default_bone(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    preference = Preference.objects.get(user=user)
    
    preference.default_bone = request.POST['default_bone']
    preference.save()

    return HttpResponse("切换默认骨骼成功")

# 修改图像亮度、对比度偏移量
def api_save_image_offset(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    dcm = DicomFile.objects.get(id=request.POST['dcm_id'])
    dcm.brightness = request.POST['brightness']
    dcm.contrast = request.POST['contrast']
    dcm.save()
    task = BoneAge.objects.get(dcm_file=dcm)
    task.save()
    return HttpResponse('已修改图像亮度对比度偏移量')

# 修改骨骼评分评级备注等详细信息
def api_modify_bone_detail(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    bone_detail_id = request.POST['id']
    bone_detail = BoneDetail.objects.get(id=bone_detail_id)
    bone_age = bone_detail.bone_age_instance
    if bone_age.allocated_to != request.user: return HttpResponseBadRequest("该任务未分配与您，无法进行操作。")
    
    bone_detail.level = int(request.POST['level'])
    bone_detail.error = int(request.POST['error'])
    bone_detail.remarks = request.POST['remarks']
    bone_detail.modify_user = request.user
    bone_detail.save()
    bone_age.save()
    return HttpResponse('成功修改骨骼信息')

# 修改骨骼定位
def api_modify_bone_position(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    bone_detail_id = request.POST['id']
    bone_detail = BoneDetail.objects.get(id=bone_detail_id)
    bone_age = bone_detail.bone_age_instance
    if bone_age.allocated_to != request.user: return HttpResponseBadRequest("该任务未分配与您，无法进行操作。")
    
    img = bone_detail.bone_age_instance.dcm_file.dcm_to_image
    lefttop_x = float(request.POST['x'])
    lefttop_y = float(request.POST['y'])
    box_width = float(request.POST['width'])
    box_height = float(request.POST['height'])
    bone_detail.center_x = (lefttop_x + box_width / 2) / img.width
    bone_detail.center_y = (lefttop_y + box_height / 2) / img.height
    bone_detail.width = box_width / img.width
    bone_detail.height = box_height / img.height
    bone_detail.modify_user = request.user
    bone_detail.error = 0
    bone_detail.save()
    return HttpResponse('成功修改骨骼标注位置')

# 修改骨龄
def api_modify_bone_age(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    bone_age_id = request.POST['id']
    bone_age = BoneAge.objects.get(id=bone_age_id)
    if bone_age.allocated_to != request.user: return HttpResponseBadRequest("该任务未分配与您，无法进行操作。")
    
    bone_age.bone_age = float(request.POST['bone_age'])
    bone_age.modify_user = request.user
    bone_age.save()
    return HttpResponse('成功修改骨龄')

# 完成任务
def api_finish_task(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    bone_age_id = request.POST['id']
    bone_age = BoneAge.objects.get(id=bone_age_id)
    if bone_age.allocated_to != request.user: return HttpResponseBadRequest("该任务未分配与您，无法进行操作。")

    if request.POST['closed'] == 'true': bone_age.closed = True
    bone_age.closed_date = datetime.now()
    bone_age.modify_user = request.user
    bone_age.save()
    return HttpResponse('任务已标记为完成')

# 上传dcm
def api_upload_dcm(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权上传dcm文件")
    broken_files = []
    sop_uid_miss_files = []
    duplicate_files = []
    for file in request.FILES.getlist('dcm_files'):
        suffix = file.name.split('.')[-1]
        if suffix != 'dcm' and suffix != 'DCM' : continue
        file.name = file.name.lower()
        new_file = DicomFile(
            dcm=File(file),
            create_user=user,
            modify_user=user,
            error=202
        )
        new_file.save()

        # 检验dcm能否读取（reader是否可以启动）
        try: reader = dcmread(new_file.dcm, force=True)
        except Exception as e:
            print(e)
            new_file.delete()
            broken_files.append(file.name)
            continue
        
        # 检验dcm能否读取sop_instance_uid
        sop_instance_uid = None
        try: sop_instance_uid = reader.SOPInstanceUID
        except Exception as e:
            print(e)
            new_file.delete()
            sop_uid_miss_files.append(file.name)
            continue
        # 以sop instance uid验证dicom是否重复
        if sop_instance_uid:
            if DicomFile.objects.filter(SOP_Instance_UID=sop_instance_uid):
                new_file.delete()
                duplicate_files.append(file.name)
                continue
        new_file.SOP_Instance_UID = sop_instance_uid
        # 挂载患者或创建新患者并挂载dcm
        patient = Patient.objects.filter(Patient_ID=reader.PatientID)
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
                new_file.delete()
                broken_files.append(file.name)
                continue
            try: Patient_ID = reader.PatientID
            except Exception as e:
                print(e) 
                new_file.delete()
                broken_files.append(file.name)
                continue
            try: sex = 'Male' if reader.PatientSex == 'M' else 'Female'
            except Exception as e:
                print(e)
                new_file.delete()
                broken_files.append(file.name)
                continue
            try: birthday = datetime.strptime(reader.PatientBirthDate,'%Y%m%d').date()
            except Exception as e:
                print(e)
                new_file.delete()
                broken_files.append(file.name)
                continue
            patient = Patient.objects.create(
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
        new_file.age = (new_file.Study_Date - new_file.patient.birthday).days / 365
        # 结束dcm校验，保存
        new_file.save()

        #创建dcm对应的boneage实例、对应的骨骼
        bone_age = BoneAge.objects.create(dcm_file=new_file, modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='Radius', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='Ulna', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='First Metacarpal', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='Third Metacarpal', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='Fifth Metacarpal', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='First Proximal Phalange', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='Third Proximal Phalange', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='Fifth Proximal Phalange', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='Third Middle Phalange', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='Fifth Middle Phalange', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='First Distal Phalange', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='Third Distal Phalange', modify_user=user)
        BoneDetail.objects.create(bone_age_instance=bone_age, name='Fifth Distal Phalange', modify_user=user)

    print(broken_files)
    print(sop_uid_miss_files)
    print(duplicate_files)

    # TODO:操作成功后单独弹出页面提示上传失败的、成功的、重复的各个文件
    return HttpResponseRedirect(reverse('BoneAge_dicom_library_admin',args=()))

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
    for dcm in dcms_to_analyze:
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
            # TODO:二分类
            dcm.error = 0
        except Exception as e:
            print(e)
            dcm.error = 415
            continue
        dcm.save()
        
        # 目标检测，录入骨骼位置
        bones = BoneDetail.objects.filter(bone_age_instance__dcm_file=dcm)
        # 所有骨骼初始化为404
        for bone in bones:
            bone.error = 404
            bone.save()
        bone_detected = object_model.infer(img_array)
        
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
        # 骨龄评级
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
        
    return HttpResponseRedirect(reverse('BoneAge_dicom_library_admin',args=()))

# 分配指定数量的任务给指定用户
def api_allocate_tasks(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权分配任务")

    user_model = get_user_model()
    user = user_model.objects.get(id=request.POST['allocate_to'])
    tasks = BoneAge.objects.filter(dcm_file__error=0).filter(closed=False).filter(allocated_to=None)
    tasks_to_allocate_count = request.POST['tasks_to_allocate_count']
    for task in tasks[0:int(tasks_to_allocate_count)]:
        task.allocated_to = user
        task.allocated_datetime = datetime.now()
        task.save()
    return HttpResponseRedirect(reverse('BoneAge_dicom_library_admin',args=()))

# 平均分配任务给所有用户
def api_allocate_tasks_random(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权分配任务")
    
    user_model = get_user_model()
    users = user_model.objects.filter(is_active=True).exclude(is_staff=True)
    users_amount = users.count()
    tasks = BoneAge.objects.filter(dcm_file__error=0).filter(closed=False).filter(allocated_to=None)
    tasks_amount = tasks.count()
    step = int(tasks_amount / users_amount)
    i = 0
    for user in users:
        tasks_for_user = tasks[i:(i+step)]
        for task in tasks_for_user:
            task.allocated_to = user
            task.allocated_datetime = datetime.now()
            task.save()
    return HttpResponseRedirect(reverse('BoneAge_dicom_library_admin',args=()))

# 导出数据
def api_export_bone_data(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权导出数据")

    tasks = BoneAge.objects.filter(closed=True)
    for task in tasks:
        bones = BoneDetail.objects.filter(bone_age_instance=task)
        image_path = task.dcm_file.dcm_to_image.path
        if not os.path.isdir('E:/CQMU/export/bone_data/'):
            os.mkdir('E:/CQMU/export/bone_data/')
        if not os.path.isdir('E:/CQMU/export/bone_data/images/'):
            os.mkdir('E:/CQMU/export/bone_data/images/')
        if not os.path.isdir('E:/CQMU/export/bone_data/labels/'):
            os.mkdir('E:/CQMU/export/bone_data/labels/')
        # 导出图片
        out_path = 'E:/CQMU/export/bone_data/images/' + str(task.id) + '.png'
        copyfile(image_path, out_path)
        # 导出标签
        out_path = 'E:/CQMU/export/bone_data/labels/' + str(task.id) + '.txt'
        with open(out_path,'w') as f:
            label_content = str(task.dcm_file.dcm) + '\t'
            label_content += str(task.dcm_file.patient.sex)
            label_content += '\t'
            label_content += str(task.dcm_file.age)
            label_content += '\n'
            for bone in bones:
                label_content += str(bone.name)
                label_content += '\t'
                label_content += str(bone.center_x)
                label_content += '\t'
                label_content += str(bone.center_y)
                label_content += '\t'
                label_content += str(bone.width)
                label_content += '\t'
                label_content += str(bone.height)
                label_content += '\t'
                label_content += str(bone.level)
                label_content += '\t'
                label_content += '\n'
            f.write(label_content)
    
    return HttpResponse(r'导出数据完毕，目录 E:/CQMU/export/bone_data/')