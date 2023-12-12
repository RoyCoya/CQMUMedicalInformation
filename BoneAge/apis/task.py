from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from BoneAge.models import Task

# 完成任务
@login_required
def finish_task(request):
    task_id = str(request.POST.get('id'))
    if not task_id: return JsonResponse({"message":"未发送任务id"}, status=400)
    try:
        task = Task.objects.get(id=task_id if task_id.isdigit() else None)
        if request.POST.get('closed') == 'true':
            task.closed = True
            task.status = 'finished'
        task.bone_age = request.POST.get('bone_age') if request.POST.get('bone_age') else -1
        task.closed_date = datetime.now()
        task.modify_user = request.user
        task.save()
        return JsonResponse({"message":"任务已标记为完成"})
    except Exception as e: return JsonResponse({"message" : f"请求失败：{e}"}, status=500)

# 收藏任务
@login_required
def mark_task(request):
    user = request.user
    task_id = str(request.POST.get('task'))

    try:
        task = Task.objects.get(id=task_id if task_id.isdigit() else None)
        
        if user != task.allocated_to: return JsonResponse({"message":"该任务未分配于您"}, status=403)
        
        task.marked = True if request.POST['marked'] == 'true' else False
        task.save()

        return JsonResponse({"message":"任务收藏状态已切换"})
    except Exception as e: JsonResponse({"message" : f"请求错误{e}"}, status=500)
