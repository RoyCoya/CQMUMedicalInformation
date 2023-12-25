from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from BoneAge.models import Task, TaskLog, BoneDetail
from BoneAge.apis.dicom import delete_base_dcm
from BoneAge.apis.standard import GetBoneAge

# comment开启

# 评测员提交任务错误审核
@login_required
def report(request):
    task_id : str = request.POST.get('id', -1)
    try:
        task = Task.objects.get(id=task_id if task_id.isdigit() else None)
        if not task: return JsonResponse({"message":"未搜索到对应任务"}, status=404)
        if task.status != 'processing': return JsonResponse({"message":'任务状态非“进行中”，请检查代码'}, status=400)
        task.status = 'reported'
        task.modify_user = request.user
        task.save()
        TaskLog.objects.create(
            task = task,
            operation = 'report',
            operator = request.user,
            comment = request.POST.get('comment'),
        )
        return JsonResponse({"message":"任务已申请错误影响审核"})
    except Exception as e: return JsonResponse({"message" : f"请求失败：{e}"}, status=500)

# 评测员提交任务完成审核
@login_required
def submit(request):
    task_id : str = request.POST.get('id', -1)
    try:
        task = Task.objects.get(id=task_id if task_id.isdigit() else None)
        if not task: return JsonResponse({"message":"未搜索到对应任务"}, status=404)
        if task.status != 'processing': return JsonResponse({"message":'任务状态非“进行中”，请检查代码'}, status=400)
        task.status = 'verifying'
        task.modify_user = request.user
        task.save()
        TaskLog.objects.create(
            task = task,
            operation = 'submit',
            operator = request.user,
            comment = request.POST.get('comment'),
        )
        return JsonResponse({"message":"任务已提交"})
    except Exception as e: return JsonResponse({"message" : f"请求失败：{e}"}, status=500)

# 评测员撤回提交
@login_required
def withdraw(request):
    task_id : str = request.POST.get('id', -1)
    try:
        task = Task.objects.get(id=task_id if task_id.isdigit() else None)
        if not task: return JsonResponse({"message":"未搜索到对应任务"}, status=404)
        if task.status not in ['reported', 'verifying']: return JsonResponse({"message":'任务状态非“等待审核”或“等待检错”，请检查代码'}, status=400)
        task.status = 'processing'
        task.modify_user = request.user
        task.save()
        TaskLog.objects.create(
            task = task,
            operation = 'withdraw',
            operator = request.user,
            comment = request.POST.get('comment'),
        )
        return JsonResponse({"message":"已撤回上次提交"})
    except Exception as e: return JsonResponse({"message" : f"请求失败：{e}"}, status=500)

@login_required
# 管理员通过再审/报错
def verify(request):
    if not request.user.is_staff: return JsonResponse({"message": "请求失败：权限不足"}, status=403)
    task_id : str = request.POST.get('id', -1)
    task = Task.objects.get(id=task_id if task_id.isdigit() else None)
    try:
        if not task: return JsonResponse({"message":"未搜索到对应任务"}, status=404)
        if task.status not in ['reported', 'verifying']: return JsonResponse({"message":'任务状态非“等待审核”或“等待检错”，请检查代码'}, status=400)
        task.status = 'finished'
        task.closed = True
        task.closed_date = datetime.now()
        task.modify_user = request.user
        task.save()
        TaskLog.objects.create(
            task = task,
            operation = 'verify',
            operator = request.user,
            comment = request.POST.get('comment'),
        )
        message = "审核已通过"
        delete_option = request.POST.get('type')
        if delete_option:
            {
                'recall' : lambda : task.delete(),
                'with_dcm' : lambda : task.dcm_file.delete(),
                'with_base_dcm' : lambda : delete_base_dcm(task.dcm_file.base_dcm),
            }[delete_option]()
            message += "，已删除任务，处理类型：" + delete_option
        
        return JsonResponse({"message":message})
    except Exception as e: return JsonResponse({"message" : f"请求失败：{e}"}, status=500)

# 管理员拒绝通过再审/报错
@login_required
def reject(request):
    if not request.user.is_staff: return JsonResponse({"message": "请求失败：权限不足"}, status=403)
    task_id : str = request.POST.get('id', -1)
    task = Task.objects.get(id=task_id if task_id.isdigit() else None)
    try:
        if not task: return JsonResponse({"message":"未搜索到对应任务"}, status=404)
        if task.status not in ['reported', 'verifying']: return JsonResponse({"message":'任务状态非“等待审核”或“等待检错”，请检查代码'}, status=400)
        task.status = 'processing'
        task.modify_user = request.user
        task.save()
        TaskLog.objects.create(
            task = task,
            operation = 'reject',
            operator = request.user,
            comment = request.POST.get('comment'),
        )
        return JsonResponse({"message" : "已拒绝通过审核"})
    except Exception as e: return JsonResponse({"message" : f"请求失败：{e}"}, status=500)

# 管理员快捷完成任务
@login_required
def finish(request):
    if not request.user.is_staff: return JsonResponse({"message": "请求失败：权限不足"}, status=403)
    task_id : str = request.POST.get('id', -1)
    try:
        task = Task.objects.get(id=task_id if task_id.isdigit() else None)
        if not task: return JsonResponse({"message":"未搜索到对应任务"}, status=404)
        if task.status != 'processing': return JsonResponse({"message":'任务状态非“进行中”，请检查代码'}, status=400)
        task.bone_age = request.POST.get('bone_age') if request.POST.get('bone_age') else GetBoneAge(
            task.standard,
            task.dcm_file.base_dcm.patient.sex,
            BoneDetail.objects.filter(task=task)
        )
        task.status = 'finished'
        task.closed = True
        task.closed_date = datetime.now()
        task.modify_user = request.user
        task.save()
        TaskLog.objects.create(
            task = task,
            operation = 'finish',
            operator = request.user,
            comment = request.POST.get('comment'),
        )
        return JsonResponse({"message":"任务已标记为完成"})
    except Exception as e: return JsonResponse({"message" : f"请求失败：{e}"}, status=500)

# 管理员重开任务
@login_required
def reopen(request):
    if not request.user.is_staff: return JsonResponse({"message": "请求失败：权限不足"}, status=403)
    task_id : str = request.POST.get('id', -1)

    task = Task.objects.get(id=task_id if task_id.isdigit() else None)
    if not task: return JsonResponse({"message":"未搜索到对应任务"}, status=404)
    if task.status != 'finished': return JsonResponse({"message":'任务状态非“进行中”，请检查代码'}, status=400)
    task.closed = False
    task.status = 'processing'
    task.modify_user = request.user
    task.save()
    TaskLog.objects.create(
        task = task,
        operation = 'reopen',
        operator = request.user,
        comment = request.POST.get('comment'),
    )
    return JsonResponse({"message":"任务重开成功"})

# 管理员删除任务
@login_required
def delete(request):
    if not request.user.is_staff: return JsonResponse({"message": "请求失败：权限不足"}, status=403)
    task_id : str = request.POST.get('id', -1)
    delete_option = request.POST.get('type', 'with_base_dcm')

    task = Task.objects.get(id=task_id if task_id.isdigit() else None)
    if not task: return JsonResponse({"message":"未搜索到对应任务"}, status=404)
    TaskLog.objects.create(
        task = task,
        operation = 'delete',
        operator = request.user,
        comment = request.POST.get('comment'),
    )
    {
        'recall' : lambda : task.delete(),
        'with_dcm' : lambda : task.dcm_file.delete(),
        'with_base_dcm' : lambda : delete_base_dcm(task.dcm_file.base_dcm),
    }[delete_option]()
    return JsonResponse({"message":"任务删除成功"})

# # 收藏任务
# @login_required
# def mark_task(request):
#     user = request.user
#     task_id = str(request.POST.get('task'))

#     try:
#         task = Task.objects.get(id=task_id if task_id.isdigit() else None)
        
#         if user != task.allocated_to: return JsonResponse({"message":"该任务未分配于您"}, status=403)
        
#         task.marked = True if request.POST['marked'] == 'true' else False
#         task.save()

#         return JsonResponse({"message":"任务收藏状态已切换"})
#     except Exception as e: JsonResponse({"message" : f"请求错误{e}"}, status=500)
