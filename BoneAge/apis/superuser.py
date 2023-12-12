import os
from shutil import copyfile

from django.conf import settings
from django.http import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from BoneAge.models import BoneDetail, Task

# 导出数据
@login_required
def export_bone_data(request):
    user = request.user
    if not user.is_staff: return HttpResponseBadRequest("您无权导出数据")

    if not os.path.isdir('E:/CQMU/export/bone_data/'):
        os.mkdir('E:/CQMU/export/bone_data/')
    tasks = Task.objects.filter(closed=True)|Task.objects.filter(allocated_to=4)
    if not os.path.isdir('E:/CQMU/export/bone_data/images/'):
        os.mkdir('E:/CQMU/export/bone_data/images/')
    if not os.path.isdir('E:/CQMU/export/bone_data/labels/'):
        os.mkdir('E:/CQMU/export/bone_data/labels/')
    for task in tasks:
        bones = BoneDetail.objects.filter(task=task)
        image_path = task.dcm_file.base_dcm.dcm_to_image.path
        # 导出图片
        out_path = 'E:/CQMU/export/bone_data/images/' + str(task.id) + '.png'
        copyfile(image_path, out_path)
        # 导出标签
        out_path = 'E:/CQMU/export/bone_data/labels/' + str(task.id) + '.txt'
        with open(out_path,'w') as f:
            label_content = str(task.dcm_file.base_dcm.dcm) + '\t'
            label_content += str(task.dcm_file.base_dcm.patient.sex)
            label_content += '\t'
            label_content += str((task.dcm_file.base_dcm.Study_Date - task.dcm_file.base_dcm.patient.birthday).days / 365)
            label_content += '\t'
            label_content +=  str(task.bone_age)
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