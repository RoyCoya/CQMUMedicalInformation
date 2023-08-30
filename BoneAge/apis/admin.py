import json
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model

from django.http import *
from django.shortcuts import redirect, render


from BoneAge.apis.Standard.BoneName import CHN, RUS_CHN
from BoneAge.apis.Standard.Converter import GetBoneAge
from BoneAge.apis.public_func import login_check
from BoneAge.apis.bone_analysis import bone_detect
from BoneAge.apis.dicom import create_dcm, delete_base_dcm
from BoneAge.models import BoneDetail, DicomFile, Task

# 手动上传dcm
def api_upload_dcm(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权上传dcm文件")
    # TODO:错误列表改成[{name:'', error:''}]形式
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
    return render(request, 'BoneAge/index/admin/upload_results.html', context)

# 任务分配
def api_allocate_tasks(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    allocator = request.user
    if not allocator.is_staff: return HttpResponseBadRequest("您无权分配任务")

    dcms_to_allocate_ids = [int(id) for id in str(request.POST['dcm_id_list']).split(' ')[0:-1]]
    dcms_to_allocate = DicomFile.objects.filter(id__in=dcms_to_allocate_ids)
    allocate_standard = json.loads(request.POST['standard_list'])
    allocated_to = get_user_model().objects.get(id=request.POST['allocated_to'])
    confidence = int(request.POST['confidence']) / 100
    
    # 当前提交的dcm状态改为“处理中”，使这些dcm在处理界面隐藏
    dcms_to_allocate.update(error = 102)

    for dcm in dcms_to_allocate: 
        for standard in allocate_standard: allocate_task(dcm, allocator, standard, allocated_to, confidence)

    return HttpResponse('任务分配成功')

def allocate_task(dcm : DicomFile, allocator, allocate_standard : str, allocated_to, confidence : float) -> bool:

    # 如果当前需要创建的任务已存在（异步时可能有冲突），则跳过
    if Task.objects.filter(dcm_file=dcm).filter(standard=allocate_standard): return 409

    # 创建任务
    new_task = Task.objects.create(
        dcm_file = dcm,
        standard = allocate_standard,
        allocated_to = allocated_to,
        allocated_datetime = datetime.now(),
        modify_user = allocator
    )
    
    # 创建骨骼信息
    bone_name_list = {
        'RUS' : lambda : RUS_CHN,
        'CHN' : lambda : CHN,
    }[new_task.standard]()
    for bone_name in bone_name_list: BoneDetail.objects.create(
        task=new_task, name=bone_name, modify_user=allocator, error=404
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
    
    detection_accuracy = 1 - sum(1 for bone in bones if bone.error != 0) / bones.count()
    if detection_accuracy < confidence:
        dcm.error = 403
        dcm.save()
        new_task.delete()
        return False
    if detection_accuracy == 1:
        new_task.bone_age = GetBoneAge(
            standard=new_task.standard,
            sex = new_task.dcm_file.base_dcm.patient.sex,
            bones = bones
        )
        new_task.save()

    dcm.error = 0
    dcm.save()

    return True

# 删除任务
# 删除方式：only_task（保留影像在DICOMManagement中）、with_source（连带删除影像）
def api_delete_tasks(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权删除任务")

    dcms_to_delete_ids = str(request.POST['dcm_id_list']).split(' ')[0:-1]
    dcms_to_delete = DicomFile.objects.filter(id__in=dcms_to_delete_ids)

    # 当前提交的dcm状态改为“处理中”，使这些dcm在处理界面隐藏
    for dcm in dcms_to_delete:
        dcm.error = 102
        dcm.save()

    for dcm in dcms_to_delete:
        {
            'only_task' : lambda : dcm.delete(),
            'with_dcm' : lambda : delete_base_dcm(dcm.base_dcm),
        }[request.POST['type']]()

    return HttpResponse('任务删除成功')