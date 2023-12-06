from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from BoneAge.models import Task
from BoneAge.apis.dicom import get_study_age
from PatientManagement.models import Patient

# 患者个人资料
@login_required
def profile(request, patient_id):
    patient = Patient.objects.get(id=patient_id)

    # 默认显示栏目
    info_tab = None
    try: info_tab = request.GET['info_tab']
    except: pass

    # 骨龄数据
    tasks_history = Task.objects.filter(dcm_file__base_dcm__patient__id=patient_id).filter(closed=True).order_by('-closed_date')
    for task in tasks_history: task.actual_age = get_study_age(task.dcm_file.base_dcm)
    tasks_processing = Task.objects.filter(dcm_file__base_dcm__patient__id=patient_id).filter(closed=False).order_by('-allocated_datetime')
    for task in tasks_processing: task.actual_age = get_study_age(task.dcm_file.base_dcm)

    context = {
        'patient' : patient,
        'tasks_history' : tasks_history,
        'tasks_processing' : tasks_processing,
        'info_tab' : info_tab,
    }
    return render(request, 'PatientManagement/profile/profile.html', context)