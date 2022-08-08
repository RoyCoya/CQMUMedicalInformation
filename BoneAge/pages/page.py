from lib2to3.pytree import convert
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import *
from django.urls import reverse
from django.core.paginator import Paginator
import datetime

from BoneAge.models import *
from BoneAge.api.api import login_check, load_preference

# 个人主页
def index(request, page_number, order, is_descend):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.user.is_staff: return dicom_library_admin(request)
    
    # 加载用户偏好
    preference = load_preference(request)

    unfinished_tasks = BoneAge.objects.filter(closed=False).filter(allocated_to=request.user)
    # 按所需排序条件对未完成任务列表进行排序
    if order > 4:
        return HttpResponseRedirect(reverse('BoneAge_index',args=(1,0,0)))
    order_para = {
        0 : lambda : 'id',
        1 : lambda : 'dcm_file__patient__Patient_ID',
        2 : lambda : 'dcm_file__age',
        3 : lambda : 'dcm_file__Study_Date',
        4 : lambda : 'allocated_datetime',
    }[order]()
    if is_descend:
        order_para = '-' + order_para
    unfinished_tasks = unfinished_tasks.order_by(order_para)
    unfinished_tasks_count = len(unfinished_tasks)
    finished_tasks = BoneAge.objects.filter(allocated_to=request.user).filter(closed=True).order_by('-closed_date')
    finished_tasks_count = len(finished_tasks)
    finished_today_count = len(finished_tasks.filter(closed_date__gt=datetime.date.today()))
    
    # 任务列表分页
    unfinished_tasks_paged = Paginator(unfinished_tasks, 15)
    unfinished_tasks_current_page = None
    try: unfinished_tasks_current_page = unfinished_tasks_paged.page(page_number)
    except: return HttpResponseBadRequest('页面错误！页码小于1或超出上限。')
    has_previous_page = unfinished_tasks_current_page.has_previous()
    has_next_page = unfinished_tasks_current_page.has_next()

    # 查询每个患者的历史评测记录数量
    for task in unfinished_tasks_current_page:
        task.history = 1

    # 完结任务大于6个折叠，跳转给完结任务界面
    if finished_tasks_count > 6:
        finished_tasks = finished_tasks[0:6]
    
    context = {
        'preference' : preference,
        'unfinished_tasks' : unfinished_tasks_current_page,
        'unfinished_tasks_count' : unfinished_tasks_count,
        'order' : order,
        'is_descend' : is_descend,
        'page_number' : page_number,
        'page_count' : unfinished_tasks_paged.num_pages,
        'has_previous_page' : has_previous_page,
        'has_next_page' : has_next_page,
        'finished_tasks' : finished_tasks,
        'finished_tasks_count' : finished_tasks_count,
        'finished_today_count' : finished_today_count,
        'page_count' : unfinished_tasks_paged.num_pages,
    }
    return render(request,'BoneAge/index/index.html',context)

# 完结任务
def finished_tasks(request, page_number, order, is_descend):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.user.is_staff: return dicom_library_admin(request)

    # 加载用户偏好
    preference = load_preference(request)

    finished_tasks = BoneAge.objects.filter(closed=True).filter(allocated_to=request.user)
    finished_today_count = len(finished_tasks.filter(closed_date__gt=datetime.date.today()))
    # 按所需排序条件对完结任务列表进行排序
    if order > 5:
        return HttpResponseRedirect(reverse('BoneAge_index',args=(1,0,0)))
    order_para = {
        0 : lambda : 'id',
        1 : lambda : 'dcm_file__patient__Patient_ID',
        2 : lambda : 'dcm_file__age',
        3 : lambda : 'dcm_file__Study_Date',
        4 : lambda : 'allocated_datetime',
        5 : lambda : 'closed_date'
    }[order]()
    if is_descend:
        order_para = '-' + order_para
    finished_tasks = finished_tasks.order_by(order_para)
    finished_tasks_count = len(finished_tasks)
    unfinished_tasks = BoneAge.objects.filter(allocated_to=request.user).filter(closed=False).order_by('id')
    unfinished_tasks_count = len(unfinished_tasks)
    
    # 完结任务列表分页
    finished_tasks_paged = Paginator(finished_tasks, 15)
    finished_tasks_current_page = None
    try: finished_tasks_current_page = finished_tasks_paged.page(page_number)
    except: return HttpResponseBadRequest('页面错误！页码小于1或超出上限。')
    has_previous_page = finished_tasks_current_page.has_previous()
    has_next_page = finished_tasks_current_page.has_next()

    # 查询每个患者的历史评测记录数量
    for task in finished_tasks_current_page:
        task.history = 1

    # 未完结任务大于6个折叠，跳转给个人主页
    if unfinished_tasks_count > 6:
        unfinished_tasks = unfinished_tasks[0:6]
    
    context = {
        'preference' : preference,
        'finished_tasks' : finished_tasks_current_page,
        'finished_tasks_count' : finished_tasks_count,
        'order' : order,
        'is_descend' : is_descend,
        'page_number' : page_number,
        'page_count' : finished_tasks_paged.num_pages,
        'has_previous_page' : has_previous_page,
        'has_next_page' : has_next_page,
        'unfinished_tasks' : unfinished_tasks,
        'unfinished_tasks_count' : unfinished_tasks_count,
        'finished_today_count' : finished_today_count,
        'page_count' : finished_tasks_paged.num_pages,
    }
    return render(request,'BoneAge/index/finished_tasks/finished_tasks.html',context)

# dicom库
def dicom_library(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    finished_tasks = BoneAge.objects.filter(closed=True)
    allocated_unfinished_tasks = BoneAge.objects.filter(dcm_file__error=0).filter(closed=False).exclude(allocated_to=None)
    context = {
        'finished_tasks' : finished_tasks,
        'unfinished_tasks' : allocated_unfinished_tasks,
    }
    return render(request,'BoneAge/dcm_library/library.html',context)

# dicom库后台
def dicom_library_admin(request):
    unanalyzed_dcm_count = DicomFile.objects.filter(error=202).count()
    unallocated_tasks = BoneAge.objects.filter(dcm_file__error=0).filter(closed=False).filter(allocated_to=None)
    user_model = get_user_model()
    users = user_model.objects.filter(is_active=True).exclude(is_staff=True)
    context = {
        'unallocated_tasks' : unallocated_tasks,
        'unanalyzed_dcm_count' : unanalyzed_dcm_count,
        'users' : users
    }
    return render(request,'BoneAge/dcm_library/admin.html', context)

# 评分器
def evaluator(request,bone_age_id):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    task = BoneAge.objects.get(id=bone_age_id)

    # 加载用户偏好
    preference = load_preference(request)
    bone_details = []
    bone_order = {
        'RUS' : lambda : preference.bone_order_RUS.split('|'),
        # 'CHN' : lambda : preference.bone_order_RUS, （未实装）
    }[preference.standard]()
    preference.bone_order = bone_order
    for bone_name in bone_order:
        try: bone_detail = BoneDetail.objects.get(name=bone_name,bone_age_instance=task)
        except Exception as e:return HttpResponseBadRequest(e)
        bone_details.append(bone_detail)

    # 上下一个任务（用于快捷键切换），若当前任务完结则以时间倒序为准，若当前任务未完成则以任务id为准
    pre_task = None
    next_task = None
    if task.closed:
        try: pre_task = BoneAge.objects.filter(allocated_to=request.user, closed=True).filter(closed_date__gt=task.closed_date).order_by('closed_date').first()
        except: pass
        try: next_task = BoneAge.objects.filter(allocated_to=request.user, closed=True).filter(closed_date__lt=task.closed_date).order_by('closed_date').last()
        except: pass
    else:
        try: pre_task = BoneAge.objects.filter(allocated_to=request.user, closed=False).filter(id__lt=task.id).last()
        except: pass
        try: next_task = BoneAge.objects.filter(allocated_to=request.user, closed=False).filter(id__gt=task.id).first()
        except: pass

    dcm = task.dcm_file
    patient = dcm.patient
    context = {
        'preference' : preference,
        'patient' : patient,
        'dcm' : dcm,
        'task' : task,
        'pre_task' : pre_task,
        'next_task' : next_task,
        'bone_details' : bone_details,
    }
    return render(request,'BoneAge/evaluator/evaluator.html',context)
