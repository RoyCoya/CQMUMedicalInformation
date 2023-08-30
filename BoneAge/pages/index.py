import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import *
from django.shortcuts import redirect, render
from django.urls import reverse

from BoneAge.apis.public_func import load_preference, login_check
from BoneAge.models import DicomFile, Task, PACS_QR

# 个人主页（未完结任务页面）
def index(request, page_number):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.user.is_staff: return HttpResponseRedirect(reverse('BoneAge_admin',args=()))
    order = 0
    is_descend = 0
    try:
        order = int(request.GET['order'])
        is_descend = int(request.GET['is_descend'])
    except: pass
    
    # 加载用户偏好
    # 自定义骨骼排序
    preference = load_preference(request)

    # 未完成任务
    unfinished_tasks = Task.objects.exclude(dcm_file__error=102).filter(standard=preference.standard).filter(closed=False).filter(allocated_to=request.user)
    # 排序参数
    if order > 4:
        return HttpResponseRedirect(reverse('BoneAge_index',args=(1,)))
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
    finished_tasks = Task.objects.filter(standard=preference.standard).filter(allocated_to=request.user).filter(closed=True).order_by('-closed_date')
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
        task.history = Task.objects.filter(dcm_file__base_dcm__patient__id=task.dcm_file.base_dcm.patient.id).filter(closed=True).count()

    # 完结任务大于6个折叠，跳转给完结任务界面
    if finished_tasks_count > 6:
        finished_tasks = finished_tasks[0:6]
    
    # 最后编辑的任务
    task_last_modified = Task.objects.filter(standard=preference.standard).filter(allocated_to=request.user).order_by('-modify_date').first()
    
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

# 完结任务页面
def finished_tasks(request, page_number, ):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.user.is_staff: return admin(request)
    order, is_descend = 5, 1
    try:
        order = int(request.GET['order'])
        is_descend = int(request.GET['is_descend'])
    except: pass
    # 加载用户偏好
    preference = load_preference(request)

    finished_tasks = Task.objects.filter(standard=preference.standard).filter(closed=True).filter(allocated_to=request.user)
    finished_today_count = len(finished_tasks.filter(closed_date__gt=datetime.date.today()))
    # 按所需排序条件对完结任务列表进行排序
    if order > 5:
        return HttpResponseRedirect(reverse('BoneAge_index',args=(1,)))
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
    unfinished_tasks = Task.objects.exclude(dcm_file__error=102).filter(standard=preference.standard).filter(allocated_to=request.user).filter(closed=False).order_by('id')
    unfinished_tasks_count = len(unfinished_tasks)
    
    # 完结任务列表分页
    finished_tasks_paged = Paginator(finished_tasks, 15)
    finished_tasks_current_page = None
    try: finished_tasks_current_page = finished_tasks_paged.page(page_number)
    except: return HttpResponseBadRequest('页面错误！页码小于1或超出上限。')
    has_previous_page = finished_tasks_current_page.has_previous()
    has_next_page = finished_tasks_current_page.has_next()

    for task in finished_tasks_current_page:
        task.history = Task.objects.filter(dcm_file__base_dcm__patient__id=task.dcm_file.base_dcm.patient.id).filter(closed=True).count() - 1

    # 未完结任务大于6个折叠，跳转给个人主页
    if unfinished_tasks_count > 6:
        unfinished_tasks = unfinished_tasks[0:6]
    
    # 最后编辑的任务
    task_last_modified = Task.objects.filter(standard=preference.standard).filter(allocated_to=request.user).order_by('-modify_date').first()

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

# 管理员页面
def admin(request):
    # 数据库状态检查
    error_dcm_count = DicomFile.objects.exclude(error=0).exclude(error=102).count()
    # TODO: 根据单一或数个标准查询未分配任务的dcm
    unallocated_dcm = DicomFile.objects.annotate(dcm_tasks=Count('BoneAge_Task_affiliated_dcm')).exclude(dcm_tasks__gt=0).filter(error__in=[0,403])
    # 可用于任务分配的账号
    user_model = get_user_model()
    evaluators = user_model.objects.filter(is_active=True).exclude(is_staff=True)
    # 远程PACS
    PACS_list = PACS_QR.objects.all()

    context = {
        'unallocated_dcm' : unallocated_dcm,
        'error_dcm_count' : error_dcm_count,
        'evaluators' : evaluators,
        'PACS_list' : PACS_list,
    }
    return render(request,'BoneAge/index/admin/admin.html', context)