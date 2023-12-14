from django.conf import settings
from django.http import *
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from BoneAge.apis.public_func import load_preference
from BoneAge.models import BoneDetail, Task
from BoneAge.apis.standard import GetJSON
from BoneAge.apis.dicom import get_study_age


# 评分器
@login_required
def evaluator(request, task_id):
    task = Task.objects.get(id=task_id)
    BoneAge_dcm = task.dcm_file
    patient = BoneAge_dcm.base_dcm.patient
    preference = load_preference(request)

    # 根据当前任务的标准，按偏好加载骨骼数据
    bone_details = []
    bone_order = getattr(preference, 'bone_order_' + task.standard).split("|")
    for bone_name in bone_order:
        try: bone_detail = BoneDetail.objects.get(name=bone_name, task=task)
        except Exception as e:
            return HttpResponseBadRequest("数据库存在骨骼信息缺失，或骨骼名字无法对应。请联系管理员检查数据库。")
        bone_details.append(bone_detail)
    preference.bone_order = bone_order

    # 加载默认骨骼
    preference.default_bone = getattr(preference, task.standard.lower() + '_default_bone')

    # 加载自定义骨龄、分数复制格式
    preference.bone_age_copy_format = getattr(preference, 'bone_age_copy_format_' + task.standard.lower())
    preference.grade_copy_format = getattr(preference, 'grade_copy_format_' + task.standard.lower())

    # 上下一个任务（用于快捷键切换），若当前任务完结则以时间倒序为准，若当前任务未完成则以任务id为准
    if task.closed:
        pre_task = (
            Task.objects.filter(standard=task.standard)
            .filter(allocated_to=request.user, closed=True)
            .filter(closed_date__gt=task.closed_date)
            .order_by("closed_date")
            .first()
        )
        next_task = (
            Task.objects.filter(standard=task.standard)
            .filter(allocated_to=request.user, closed=True)
            .filter(closed_date__lt=task.closed_date)
            .order_by("closed_date")
            .last()
        )
    else:
        pre_task = (
            Task.objects.filter(standard=task.standard)
            .filter(allocated_to=request.user, closed=False)
            .filter(id__lt=task.id)
            .last()
        )
        next_task = (
            Task.objects.filter(standard=task.standard)
            .filter(allocated_to=request.user, closed=False)
            .filter(id__gt=task.id)
            .first()
        )

    # 历史记录
    historys = (
        Task.objects.filter(
            dcm_file__base_dcm__patient__id=task.dcm_file.base_dcm.patient.id
        )
        .filter(closed=True)
        .count()
    )

    # 修复骨骼时刷新页面的骨骼
    bone_fixed = request.GET.get("bone_fixed")

    # 计算task当时患者的实际年龄
    task.actual_age = get_study_age(task.dcm_file.base_dcm)

    # 加载骨龄标准的内容
    standard = GetJSON(task.standard)

    context = {
        "preference": preference,
        "patient": patient,
        "dcm": BoneAge_dcm,
        "task": task,
        "pre_task": pre_task,
        "next_task": next_task,
        "bone_details": bone_details,
        "historys": historys,
        "bone_fixed": bone_fixed,
        "standard": standard,
    }
    return render(request, "BoneAge/evaluator/evaluator.html", context)
