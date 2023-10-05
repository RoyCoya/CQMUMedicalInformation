from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

from BoneAge.apis.public_func import login_check
from BoneAge.models import Task
from PatientManagement.models import Patient

# 患者个人资料
def profile(request, patient_id):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    patient = Patient.objects.get(id=patient_id)

    # 前一页面（页面唯一name+参数args组装reverse，else_get传其他可能需要的参数）
    back_page = back_page_get = back_page_args_get = back_page_else_get = None
    try: back_page_get = request.GET['back_page']
    except: pass
    try: back_page_args_get = tuple(request.GET.getlist('args'))
    except: pass
    try: back_page_else_get = request.GET['else_get']
    except: pass
    try:
        back_page = reverse(back_page_get,args=back_page_args_get) + '?'
        if back_page_else_get:
            back_page += back_page_else_get
    except: pass

    # 默认显示栏目
    info_tab = None
    try: info_tab = request.GET['info_tab']
    except: pass

    # 骨龄资料
    tasks_history = Task.objects.filter(dcm_file__base_dcm__patient__id=patient_id).filter(closed=True).order_by('-closed_date')
    tasks_processing = Task.objects.filter(dcm_file__base_dcm__patient__id=patient_id).filter(closed=False).order_by('-allocated_datetime')
    for task in tasks_processing:
        task.actual_age = (task.dcm_file.base_dcm.Study_Date - patient.birthday).days / 365

    context = {
        'patient' : patient,
        'tasks_history' : tasks_history,
        'tasks_processing' : tasks_processing,
        'back_page' : back_page,
        'back_page_get' : back_page_get,
        'back_page_args_get' : back_page_args_get,
        'back_page_else_get' : back_page_else_get,
        'info_tab' : info_tab,
    }
    return render(request, 'PatientManagement/profile/profile.html', context)