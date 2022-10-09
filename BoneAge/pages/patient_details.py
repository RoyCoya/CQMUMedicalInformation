from multiprocessing import context
from django.shortcuts import render, redirect
from django.conf import settings

from BoneAge.apis.public_func import login_check
from BoneAge.models import Task

from PatientManagement.models import Patient

# 患者个人资料
def profile(request, patient_id):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    patient = Patient.objects.get(id=patient_id)
    tasks = Task.objects.filter(dcm_file__base_dcm__patient__id=patient_id)

    context = {
        'patient' : patient,
        'tasks_history' : tasks,
    }
    return render(request, 'BoneAge/patient_details/profile/profile.html', context)