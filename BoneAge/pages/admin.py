from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from BoneAge.models import DicomFile, PACS_QR, Task, TaskLog
from BoneAge.apis.public_func import load_preference

# 管理员页面
@login_required
def admin(request):
    user = request.user
    if not user.is_staff: return JsonResponse({"message":"访问权限不足"}, status=403)
    preference = load_preference(request)
    unchecked_tasks = Task.objects.filter(
        status__in=['reported', 'verifying'],
        allocator = request.user
    )
    for task in unchecked_tasks: task.newest_log = TaskLog.objects.filter(task=task ,operation__in=['submit', 'report']).latest('create_time')
    unallocated_tasks = DicomFile.objects.annotate(dcm_tasks=Count('BoneAge_Task_affiliated_dcm')).exclude(dcm_tasks__gt=0).filter(error__in=[0,403]).filter(create_user=request.user)

    # 可用于任务分配的账号
    user_model = get_user_model()
    evaluators = user_model.objects.filter(is_active=True).exclude(is_staff=True)
    # 远程PACS
    PACS_list = PACS_QR.objects.all()

    context = {
        'preference' : preference,
        'unchecked_tasks' : unchecked_tasks,
        'unallocated_tasks' : unallocated_tasks,
        'evaluators' : evaluators,
        'PACS_list' : PACS_list,
    }
    return render(request,'BoneAge/admin/admin.html', context)