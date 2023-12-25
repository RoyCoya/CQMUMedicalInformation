from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from BoneAge.models import BoneDetail, DicomFile, Task, TaskLog
from BoneAge.apis.standard import GetBoneAge


# 修改图像亮度、对比度偏移量
@login_required
def save_image_offset(request):
    BoneAge_dcm = DicomFile.objects.get(id=request.POST['dcm_id'])
    BoneAge_dcm.brightness = request.POST.get('brightness', BoneAge_dcm.brightness)
    BoneAge_dcm.contrast = request.POST.get('contrast', BoneAge_dcm.contrast)
    BoneAge_dcm.save()
    task = Task.objects.get(dcm_file=BoneAge_dcm)
    task.modify_user = request.user
    task.save()
    comment = (
        " 将 亮度 设置为 " + 
        BoneAge_dcm.brightness + "%，" + "对比度 设置为 " +
        BoneAge_dcm.contrast + "%"
    )
    TaskLog.objects.create(
        task = task,
        operation = 'update',
        operator = request.user,
        comment = comment,
    )
    return JsonResponse({'message': '已修改图像亮度对比度偏移量'})

# 修改骨骼评分评级备注等详细信息
@login_required
def modify_bone_detail(request):
    bone_detail_id = request.POST.get('id')
    bone_detail = BoneDetail.objects.get(id=bone_detail_id)
    if not bone_detail: return JsonResponse({'message': f'未找到id为{bone_detail_id}的骨骼信息'}, status=404) 
    task = bone_detail.task
    assessment = request.POST.get('level', -1)
    error = request.POST.get('error', 0)
    remarks = request.POST.get('remarks')
    
    bone_detail.assessment = assessment
    bone_detail.error = error
    bone_detail.remarks = remarks
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
    comment = (
        " 将 " + 
        bone_detail.get_name_display() + " 设置为 " + 
        bone_detail.assessment + "级"
    )
    if remarks: comment += " ，备注：" + remarks
    TaskLog.objects.create(
        task = task,
        operation = 'update',
        operator = request.user,
        comment = comment,
    )
    return JsonResponse({'message': '成功修改骨骼信息'})

# 修改骨骼定位
@login_required
def modify_bone_position(request):
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
    comment = (
        " 将" + bone_detail.get_name_display() + " 位置设置为：\n" + 
        "中心x：" + str(bone_detail.center_x) + "\n" +
        "中心y：" + str(bone_detail.center_y) + "\n" +
        "宽：" + str(bone_detail.width) + "\n" +
        "高：" + str(bone_detail.height)
    )
    TaskLog.objects.create(
        task = task,
        operation = 'update',
        operator = request.user,
        comment = comment,
    )
    return JsonResponse({'message': '成功修改骨骼标注位置'})
