from django.conf import settings
from django.http import *
from django.shortcuts import redirect, render
from django.urls import reverse

from BoneAge.apis.public_func import load_preference, login_check
from BoneAge.models import BoneDetail, Task

# 评分器
def evaluator(request, task_id):
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

    # 历史记录
    historys = Task.objects.filter(dcm_file__base_dcm__patient__id=task.dcm_file.base_dcm.patient.id).filter(closed=True).count()

    # 前一页面
    back_page = back_page_get = back_page_args_get = back_page_else_get = None
    try: back_page_get = request.GET['back_page']
    except Exception as e: print(e)
    try: back_page_args_get = tuple(request.GET.getlist('args'))
    except Exception as e: print(e)
    try: back_page_else_get = request.GET['else_get']
    except Exception as e: print(e)
    try:
        back_page = reverse(back_page_get,args=back_page_args_get) + '?'
        if back_page_else_get:
            back_page += back_page_else_get
    except Exception as e: print(e)

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
        'historys' : historys,
        'back_page' : back_page,
        'back_page_get' : back_page_get,
        'back_page_args_get' : back_page_args_get,
        'back_page_else_get' : back_page_else_get,
    }
    return render(request,'BoneAge/evaluator/evaluator.html',context)
