import datetime
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import *
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from BoneAge.apis.public_func import login_check, load_preference
from BoneAge.models import Task, DicomFile

# 个人主页（未完结任务）
def index(request, page_number):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.user.is_staff: return dicom_library_admin(request)
    order = 0
    is_descend = 0
    try:
        order = int(request.GET['order'])
        is_descend = int(request.GET['is_descend'])
    except: pass
    
    # 加载用户偏好
    preference = load_preference(request)

    # 未完成任务
    unfinished_tasks = Task.objects.filter(closed=False).filter(allocated_to=request.user)
    # 排序参数
    if order > 4:
        return HttpResponseRedirect(reverse('BoneAge_index',args=(1)))
    order_para = {
        0 : lambda : 'id',
        1 : lambda : 'dcm_file__base_dcm__patient__Patient_ID',
        # TODO:想个办法把age排序做出来
        # 2 : lambda : 'dcm_file__age',
        3 : lambda : 'dcm_file__base_dcm__Study_Date',
        4 : lambda : 'allocated_datetime',
    }[order]()
    if is_descend:
        order_para = '-' + order_para
    unfinished_tasks = unfinished_tasks.order_by(order_para)
    unfinished_tasks_count = len(unfinished_tasks)
    # 已完结任务
    finished_tasks = Task.objects.filter(allocated_to=request.user).filter(closed=True).order_by('-closed_date')
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
    
    # 最后编辑的任务
    task_last_modified = Task.objects.filter(allocated_to=request.user).order_by('-modify_date').first()
    
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
        'task_last_modified' : task_last_modified,
    }
    return render(request,'BoneAge/index/index.html',context)

# 完结任务
def finished_tasks(request, page_number, ):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.user.is_staff: return dicom_library_admin(request)
    order, is_descend = 4, 1
    try:
        order = int(request.GET['order'])
        is_descend = int(request.GET['is_descend'])
    except: pass
    # 加载用户偏好
    preference = load_preference(request)

    finished_tasks = Task.objects.filter(closed=True).filter(allocated_to=request.user)
    finished_today_count = len(finished_tasks.filter(closed_date__gt=datetime.date.today()))
    # 按所需排序条件对完结任务列表进行排序
    if order > 5:
        return HttpResponseRedirect(reverse('BoneAge_index',args=(1)))
    order_para = {
        0 : lambda : 'id',
        1 : lambda : 'dcm_file__base_dcm__patient__Patient_ID',
        # TODO:想个办法把age排序做出来
        # 2 : lambda : 'dcm_file__age',
        3 : lambda : 'dcm_file__base_dcm__Study_Date',
        4 : lambda : 'allocated_datetime',
        5 : lambda : 'closed_date'
    }[order]()
    if is_descend:
        order_para = '-' + order_para
    finished_tasks = finished_tasks.order_by(order_para)
    finished_tasks_count = len(finished_tasks)
    unfinished_tasks = Task.objects.filter(allocated_to=request.user).filter(closed=False).order_by('id')
    unfinished_tasks_count = len(unfinished_tasks)
    
    # 完结任务列表分页
    finished_tasks_paged = Paginator(finished_tasks, 15)
    finished_tasks_current_page = None
    try: finished_tasks_current_page = finished_tasks_paged.page(page_number)
    except: return HttpResponseBadRequest('页面错误！页码小于1或超出上限。')
    has_previous_page = finished_tasks_current_page.has_previous()
    has_next_page = finished_tasks_current_page.has_next()

    #TODO: 查询每个患者的历史评测记录数量
    for task in finished_tasks_current_page:
        task.history = 1

    # 未完结任务大于6个折叠，跳转给个人主页
    if unfinished_tasks_count > 6:
        unfinished_tasks = unfinished_tasks[0:6]
    
    # 最后编辑的任务
    task_last_modified = Task.objects.filter(allocated_to=request.user).order_by('-modify_date').first()

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

# dicom库后台
def dicom_library_admin(request):
    unanalyzed_dcm_count = DicomFile.objects.filter(error=202).count()
    unallocated_tasks = Task.objects.filter(dcm_file__error=0).filter(closed=False).filter(allocated_to=None)
    user_model = get_user_model()
    # 可用于任务分配的账号
    users = user_model.objects.filter(is_active=True).exclude(is_staff=True)
    context = {
        'unallocated_tasks' : unallocated_tasks,
        'unanalyzed_dcm_count' : unanalyzed_dcm_count,
        'users' : users
    }
    return render(request,'BoneAge/index/admin.html', context)