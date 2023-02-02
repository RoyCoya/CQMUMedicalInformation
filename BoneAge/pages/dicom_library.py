from django.conf import settings
from django.shortcuts import redirect, render

from BoneAge.apis.public_func import login_check
from BoneAge.models import Task

# dicom库
def dicom_library(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    finished_tasks = Task.objects.filter(closed=True)
    allocated_unfinished_tasks = Task.objects.filter(dcm_file__error=0).filter(closed=False).exclude(allocated_to=None)
    context = {
        'finished_tasks' : finished_tasks,
        'unfinished_tasks' : allocated_unfinished_tasks,
    }
    return render(request,'BoneAge/dcm_library/library.html',context)