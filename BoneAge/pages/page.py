from traceback import print_tb
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import *
from django.core.paginator import Paginator
import datetime

from BoneAge.models import *
from BoneAge.api.api import login_check

# 个人主页
def index(request, page_number):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.user.is_staff: return dicom_library_admin(request)
    unfinished_tasks = BoneAge.objects.filter(closed=False).filter(allocated_to=request.user).order_by('id')
    unfinished_tasks_count = len(unfinished_tasks)
    finished_tasks = BoneAge.objects.filter(allocated_to=request.user).filter(closed=True).order_by('-closed_date')
    finished_tasks_count = len(finished_tasks)
    finished_today_count = len(finished_tasks.filter(closed_date__gt=datetime.date.today()))
    
    unfinished_tasks_paged = Paginator(unfinished_tasks, 15)
    print(unfinished_tasks_paged)
    unfinished_tasks_current_page = None
    try: unfinished_tasks_current_page = unfinished_tasks_paged.page(page_number)
    except: return HttpResponseBadRequest('页面错误！页码小于1或超出上限。')
    has_previous_page = unfinished_tasks_current_page.has_previous()
    has_next_page = unfinished_tasks_current_page.has_next()

    # 查询每个患者的历史评测记录数量
    for task in unfinished_tasks:
        task.history = 1

    # 完结任务大于6个折叠，跳转给完结任务界面
    if finished_tasks_count > 6:
        finished_tasks = finished_tasks[0:6]
    
    context = {
        'unfinished_tasks' : unfinished_tasks_current_page,
        'unfinished_tasks_count' : unfinished_tasks_count,
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
    bone_age = BoneAge.objects.get(id=bone_age_id)

    dcm = bone_age.dcm_file
    patient = dcm.patient
    actual_age = dcm.Study_Date - patient.birthday
    bone_details = BoneDetail.objects.filter(bone_age_instance=bone_age)
    context = {
        'patient' : patient,
        'dcm' : dcm,
        'bone_age_instance' : bone_age,
        'bone_details' : bone_details,
        'actual_age' : actual_age.days / 365,
    }
    return render(request,'BoneAge/evaluator/evaluator.html',context)
