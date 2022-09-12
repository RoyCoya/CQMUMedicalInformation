from django.shortcuts import redirect,render
from django.conf import settings
from BoneAge.apis.public_func import login_check, load_preference
from django.http import *

from BoneAge.models import Task, BoneDetail

# 评分器
def evaluator(request,task_id):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    task = Task.objects.get(id=task_id)

    # 加载用户偏好
    preference = load_preference(request)
    bone_details = []
    bone_order = {
        'RUS' : lambda : preference.bone_order_RUS.split('|'),
        # 'CHN' : lambda : preference.bone_order_RUS, （未实装）
    }[preference.standard]()
    preference.bone_order = bone_order
    for bone_name in bone_order:
        try: bone_detail = BoneDetail.objects.get(name=bone_name,task=task)
        except Exception as e:return HttpResponseBadRequest(e)
        bone_details.append(bone_detail)

    # 上下一个任务（用于快捷键切换），若当前任务完结则以时间倒序为准，若当前任务未完成则以任务id为准
    pre_task = None
    next_task = None
    if task.closed:
        try: pre_task = Task.objects.filter(allocated_to=request.user, closed=True).filter(closed_date__gt=task.closed_date).order_by('closed_date').first()
        except: pass
        try: next_task = Task.objects.filter(allocated_to=request.user, closed=True).filter(closed_date__lt=task.closed_date).order_by('closed_date').last()
        except: pass
    else:
        try: pre_task = Task.objects.filter(allocated_to=request.user, closed=False).filter(id__lt=task.id).last()
        except: pass
        try: next_task = Task.objects.filter(allocated_to=request.user, closed=False).filter(id__gt=task.id).first()
        except: pass

    BoneAge_dcm = task.dcm_file
    patient = BoneAge_dcm.base_dcm.patient
    context = {
        'preference' : preference,
        'patient' : patient,
        'dcm' : BoneAge_dcm,
        'task' : task,
        'pre_task' : pre_task,
        'next_task' : next_task,
        'bone_details' : bone_details,
    }
    return render(request,'BoneAge/evaluator/evaluator.html',context)
