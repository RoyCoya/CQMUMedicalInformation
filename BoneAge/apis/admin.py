import json
import traceback
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import *
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from BoneAge.apis.standard import GetBoneAge, GetBoneName
from BoneAge.apis.bone_analysis import bone_detect
from BoneAge.apis.dicom import create_dcm, delete_base_dcm
from BoneAge.models import BoneDetail, DicomFile, Task, TaskLog

# 手动上传dcm
@login_required
def upload_dcm(request):
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权上传dcm文件")
    success_files = []
    broken_files = []
    duplicate_files = []
    img_convert_failed_files = []
    not_dcm_files = []
    
    # 上传
    for file in request.FILES.getlist('dcm_files'):
        new_file, error_code = create_dcm(file, user, prefix='upload')
        if new_file: success_files.append(file.name)
        else: {
                400 : lambda : broken_files.append(file.name),
                409 : lambda : duplicate_files.append(file.name),
                415 : lambda : not_dcm_files.append(file.name),
                422 : lambda : img_convert_failed_files.append(file.name),
            }[error_code]()
    
    context = {
        'success_files' : success_files,
        'broken_files' : broken_files,
        'duplicate_files' : duplicate_files,
        'img_convert_failed_files' : img_convert_failed_files,
    }
    return render(request, 'BoneAge/admin/upload_results.html', context)

# 任务分配
@login_required
def allocate_tasks(request):
    allocator = request.user
    if not allocator.is_staff: return JsonResponse({"message": "请求失败：权限不足"}, status=403)

    try:
        dcms_to_allocate_ids = [int(id) for id in str(request.POST.get('dcm_id_list', [])).split(' ')[0:-1] if id.isdigit()]
        dcms_to_allocate = DicomFile.objects.filter(id__in=dcms_to_allocate_ids)
        allocate_standard = json.loads(request.POST.get('standard_list', []))
        allocated_to_id = request.POST.get('allocated_to')
        if not str(allocated_to_id).isdigit(): return JsonResponse({"message": '分配id出错'}, status=400)
        allocated_to = get_user_model().objects.get(id=int(allocated_to_id))
        confidence = int(request.POST['confidence']) / 100
        
        # 当前提交的dcm状态改为“处理中”，使这些dcm在处理界面隐藏
        dcms_to_allocate.update(error = 102)

        success_allocated = []
        error_allocated = []
        for dcm in dcms_to_allocate: 
            for standard in allocate_standard: 
                try:
                    allocate_task(dcm, allocator, standard, allocated_to, confidence)
                    success_allocated.append(dcm)
                except Exception as e:
                    print(traceback.format_exc())
                    error_allocated.append(str(dcm) + ":" + str(e))
        success_response = "成功分配：" + str(success_allocated) + "\n"
        error_response = "分配出错：" + str(error_allocated) + "\n"
        response = success_response + error_response
        return JsonResponse({"message": f"请求成功\n{response}"})
    except Exception as e: return JsonResponse({"message": f"请求失败：{str(e)}"}, status=500)

def allocate_task(dcm : DicomFile, allocator, allocate_standard : str, allocated_to, confidence : float, delete_with_source = False) -> bool:
    # 如果当前需要创建的任务已存在（异步时可能有冲突），则跳过
    if Task.objects.filter(dcm_file=dcm).filter(standard=allocate_standard): raise ValidationError('任务已经存在，无法重复添加')

    # 创建任务
    new_task = Task.objects.create(
        dcm_file = dcm,
        standard = allocate_standard,
        modify_user = allocator,
        allocator = allocator,
    )
    
    # 创建骨骼信息
    bone_name_list = GetBoneName(new_task.standard)
    for bone_name in bone_name_list: BoneDetail.objects.create(
        task=new_task, name=bone_name, modify_user=allocator, error=404
    )
    
    bone_detected = bone_detect(dcm.base_dcm.dcm_to_image.path, allocate_standard)
    bones = BoneDetail.objects.filter(task=new_task)

    new_bone_details = []
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
            new_bone_details.append(bone)
        except: pass
    
    detection_accuracy = 1 - sum(1 for bone in bones if bone.error != 0) / bones.count()
    
    if detection_accuracy < confidence:
        dcm.error = 403
        dcm.save()
        new_task.delete()
        if delete_with_source: delete_base_dcm(new_task.dcm_file.base_dcm)
        raise ValidationError("识别为非手骨图像")
    
    if detection_accuracy == 1:
        bone_age = GetBoneAge(
            standard=new_task.standard,
            sex = new_task.dcm_file.base_dcm.patient.sex,
            bones = bones
        )
        if not bone_age:
            dcm.error = 500
            dcm.save()
            new_task.delete()
            if delete_with_source: delete_base_dcm(new_task.dcm_file.base_dcm)
            raise ValidationError("结算骨龄出错")
        new_task.bone_age = bone_age
        new_task.save()

    new_task.allocated_to = allocated_to
    new_task.allocated_datetime = datetime.now()
    new_task.save()
    dcm.error = 0
    dcm.save()

    comment = "AI评测结果：\n"
    for bone_detail in new_bone_details: comment += (
        bone_detail.get_name_display() + "：" +
        str(bone_detail.assessment) + "级\n"
    )

    TaskLog.objects.create(
        task = new_task,
        operation = 'create',
        operator = allocator,
        comment = comment,
    )
    return True

# 删除任务
# 删除方式：only_task（保留影像在DICOMManagement中）、with_source（连带删除影像）
@login_required
def delete_tasks(request):
    if not request.user.is_staff: return JsonResponse({"message": "请求失败：权限不足"}, status=403)

    dcms_to_delete_ids = str(request.POST.get('dcm_id_list')).split(' ')[0:-1]
    dcms_to_delete = DicomFile.objects.filter(id__in=dcms_to_delete_ids)

    # 当前提交的dcm状态改为“处理中”，使这些dcm在处理界面隐藏
    for dcm in dcms_to_delete:
        dcm.error = 102
        dcm.save()

    for dcm in dcms_to_delete:
        {
            'only_task' : lambda : dcm.delete(),
            'with_dcm' : lambda : delete_base_dcm(dcm.base_dcm),
        }[request.POST.get('type', 'with_dcm')]()
    
    dcms_to_delete_ids = "，".join(dcms_to_delete_ids)
    return JsonResponse({"message": f"删除成功，id：{dcms_to_delete_ids}"})
