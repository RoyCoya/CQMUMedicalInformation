from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import *

from BoneAge.models import *
from BoneAge.api.api import login_check

# 个人主页
def index(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    unfinished_tasks = BoneAge.objects.filter(closed=False).filter(allocated_to=request.user).order_by('-dcm_file__Study_Date')
    finished_tasks = BoneAge.objects.filter(allocated_to=request.user).filter(closed=True).order_by('-dcm_file__Study_Date')
    context = {
        'unfinished_tasks' : unfinished_tasks,
        'finished_tasks' : finished_tasks,
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
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if not request.user.is_staff: return HttpResponseBadRequest("您无权查看此页面")
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
    bone_details = BoneDetail.objects.filter(bone_age_instance=bone_age)
    selected_bone = None
    try:
        selected_bone = request.GET['selected_bone']
    except:
        pass
    context = {
        'patient' : patient,
        'dcm' : dcm,
        'bone_age_instance' : bone_age,
        'bone_details' : bone_details,
        'selected_bone' : selected_bone,
    }
    return render(request,'BoneAge/evaluator/evaluator.html',context)
