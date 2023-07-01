from django.conf import settings
from django.shortcuts import redirect, render

from BoneAge.apis.public_func import login_check
from BoneAge.models import Task

# dicom库
def dicom_library(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    tasks = Task.objects.all()

    context = {
        'tasks' : tasks,
    }
    return render(request,'BoneAge/dcm_library/dcm_library.html',context)