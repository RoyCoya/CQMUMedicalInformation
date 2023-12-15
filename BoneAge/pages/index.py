import datetime

from django.conf import settings
from django.core.paginator import Paginator
from django.http import *
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from BoneAge.apis.public_func import load_preference
from BoneAge.models import Task

# 个人主页（未完结任务页面）
@login_required
def index(request, page_number):
    # 加载用户偏好
    preference = load_preference(request)
    order = 0
    is_descend = 0
    standard = request.GET['standard'] if request.GET.get('standard') else preference.standard
    try:
        order = int(request.GET['order'])
        is_descend = int(request.GET['is_descend'])
    except: pass
    
    # 未完成任务
    unfinished_tasks = Task.objects.exclude(dcm_file__error=102).filter(standard=standard).filter(closed=False).filter(allocated_to=request.user)
    # 排序参数
    if order > 4:
        return HttpResponseRedirect(reverse('BoneAge_index',args=(1,)))
    order_para = {
        0 : lambda : 'id',
        1 : lambda : 'dcm_file__base_dcm__patient__Patient_ID',
        2 : lambda : 'dcm_file__base_dcm__study_age',
        3 : lambda : 'dcm_file__base_dcm__Study_Date',
        4 : lambda : 'allocated_datetime',
    }[order]()
    if is_descend: order_para = '-' + order_para
    unfinished_tasks = unfinished_tasks.order_by(order_para)
    unfinished_tasks_count = len(unfinished_tasks)

    # 已完结任务
    finished_tasks = Task.objects.filter(standard=standard).filter(allocated_to=request.user).filter(closed=True).order_by('-closed_date')
    finished_tasks_count = len(finished_tasks)
    finished_today_count = len(finished_tasks.filter(closed_date__gt=datetime.date.today()))
    
    # 任务列表分页
    unfinished_tasks_paged = Paginator(unfinished_tasks, 15)
    unfinished_tasks_current_page = None
    try: unfinished_tasks_current_page = unfinished_tasks_paged.page(page_number)
    except: return HttpResponseBadRequest('页面错误！页码小于1或超出上限。')
    has_previous_page = unfinished_tasks_current_page.has_previous()
    has_next_page = unfinished_tasks_current_page.has_next()

    # 给当前页面的任务补充历史记录计数
    for task in unfinished_tasks_current_page:
        task.history = Task.objects.filter(dcm_file__base_dcm__patient__id=task.dcm_file.base_dcm.patient.id).filter(closed=True).count()

    # 完结任务大于6个折叠，跳转给完结任务界面
    if finished_tasks_count > 6:
        finished_tasks = finished_tasks[0:6]
    
    # 最后编辑的任务
    task_last_modified = Task.objects.filter(standard=standard).filter(allocated_to=request.user).order_by('-modify_date').first()
    
    context = {
        'preference' : preference,
        'standard' : standard,
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
        'task_last_modified' : task_last_modified,
    }
    return render(request,'BoneAge/index/index.html',context)

# 完结任务页面
@login_required
def finished_tasks(request, page_number):
    order, is_descend = 5, 1
    try:
        order = int(request.GET['order'])
        is_descend = int(request.GET['is_descend'])
    except: pass
    # 加载用户偏好
    preference = load_preference(request)
    standard = request.GET['standard'] if request.GET.get('standard') else preference.standard

    finished_tasks = Task.objects.filter(standard=standard).filter(closed=True).filter(allocated_to=request.user)
    finished_today_count = len(finished_tasks.filter(closed_date__gt=datetime.date.today()))
    # 按所需排序条件对完结任务列表进行排序
    if order > 5 or order < 0: return HttpResponseRedirect(reverse('BoneAge_index',args=(1,)))
    order_para = {
        0 : lambda : 'id',
        1 : lambda : 'dcm_file__base_dcm__patient__Patient_ID',
        2 : lambda : 'dcm_file__base_dcm__study_age',
        3 : lambda : 'dcm_file__base_dcm__Study_Date',
        4 : lambda : 'allocated_datetime',
        5 : lambda : 'closed_date'
    }[order]()
    if is_descend: order_para = '-' + order_para
    finished_tasks = finished_tasks.order_by(order_para)
    finished_tasks_count = len(finished_tasks)
    unfinished_tasks = Task.objects.exclude(dcm_file__error=102).filter(standard=standard).filter(allocated_to=request.user).filter(closed=False).order_by('id')
    unfinished_tasks_count = len(unfinished_tasks)
    
    # 完结任务列表分页
    finished_tasks_paged = Paginator(finished_tasks, 15)
    finished_tasks_current_page = None
    try: finished_tasks_current_page = finished_tasks_paged.page(page_number)
    except: return HttpResponseBadRequest('页面错误！页码小于1或超出上限。')
    has_previous_page = finished_tasks_current_page.has_previous()
    has_next_page = finished_tasks_current_page.has_next()

    # 给当前页面的任务补充历史记录计数
    for task in finished_tasks_current_page:
        task.history = Task.objects.filter(dcm_file__base_dcm__patient__id=task.dcm_file.base_dcm.patient.id).filter(closed=True).count() - 1

    # 未完结任务大于6个折叠，跳转给个人主页
    if unfinished_tasks_count > 6:
        unfinished_tasks = unfinished_tasks[0:6]
    
    # 最后编辑的任务
    task_last_modified = Task.objects.filter(standard=standard).filter(allocated_to=request.user).order_by('-modify_date').first()

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
        'task_last_modified' : task_last_modified,
    }
    return render(request,'BoneAge/index/finished_tasks/finished_tasks.html',context)