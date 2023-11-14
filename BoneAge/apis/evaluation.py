from django.conf import settings
from django.http import *
from django.shortcuts import redirect

from BoneAge.apis.public_func import login_check
from BoneAge.models import BoneDetail, DicomFile, Task
from BoneAge.apis.standard import GetBoneAge


# 修改图像亮度、对比度偏移量
def api_save_image_offset(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    BoneAge_dcm = DicomFile.objects.get(id=request.POST['dcm_id'])
    BoneAge_dcm.brightness = request.POST['brightness']
    BoneAge_dcm.contrast = request.POST['contrast']
    BoneAge_dcm.save()
    task = Task.objects.get(dcm_file=BoneAge_dcm)
    task.modify_user = request.user
    task.save()
    return HttpResponse('已修改图像亮度对比度偏移量')

# 修改骨骼评分评级备注等详细信息
def api_modify_bone_detail(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    bone_detail_id = request.POST['id']
    bone_detail = BoneDetail.objects.get(id=bone_detail_id)
    task = bone_detail.task
    
    bone_detail.assessment = int(request.POST['level'])
    bone_detail.error = int(request.POST['error'])
    bone_detail.remarks = request.POST['remarks']
    bone_detail.modify_user = request.user
    bone_detail.save()

    bones = BoneDetail.objects.filter(task=task)
    task.bone_age = GetBoneAge(
            standard=task.standard,
            sex = task.dcm_file.base_dcm.patient.sex,
            bones = bones
    )
    task.modify_user = request.user
    task.save()
    return HttpResponse('成功修改骨骼信息')

# 修改骨骼定位
def api_modify_bone_position(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    bone_detail_id = request.POST['id']
    bone_detail = BoneDetail.objects.get(id=bone_detail_id)
    task = bone_detail.task
    
    img = task.dcm_file.base_dcm.dcm_to_image
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
    task.modify_user = request.user
    task.save()
    return HttpResponse('成功修改骨骼标注位置')

# 修改骨龄
def api_modify_bone_age(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    task_id = request.POST['id']
    task = Task.objects.get(id=task_id)
    
    task.bone_age = float(request.POST['bone_age'])
    task.modify_user = request.user
    task.save()
    return HttpResponse('成功修改骨龄')
