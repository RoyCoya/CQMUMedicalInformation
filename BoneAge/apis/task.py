from datetime import datetime

from django.conf import settings
from django.http import *
from django.shortcuts import redirect

from BoneAge.apis.public_func import login_check
from BoneAge.models import Task

# 完成任务
def api_finish_task(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    task_id = request.POST['id']
    task = Task.objects.get(id=task_id)

    if request.POST['closed'] == 'true': task.closed = True
    print(request.POST['bone_age'])
    task.bone_age = request.POST['bone_age']
    task.closed_date = datetime.now()
    task.modify_user = request.user
    task.save()
    return HttpResponse('任务已标记为完成')

# 收藏任务
def api_mark_task(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    task = Task.objects.get(id=request.POST['task'])
    user = request.user
    if user != task.allocated_to: return HttpResponseBadRequest("该任务未分配于您")
    
    task.marked = True if request.POST['marked'] == 'true' else False
    task.save()

    return HttpResponse('任务收藏状态已切换')
