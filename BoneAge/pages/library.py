from urllib.parse import parse_qs, urlencode

from django.conf import settings
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from BoneAge.models import Task
from PatientManagement.models import Patient


# 所有记录
@login_required
def library(request):
    query = request.GET

    # 筛选结果
    tasks = Task.objects.all()
    tasks = tasks.filter(status=query.get("status")) if query.get("status") else tasks
    tasks = tasks.filter(allocator=get_user_model().objects.get(username=query.get('allocator'))) if query.get('allocator') else tasks
    tasks = tasks.filter(allocated_to=get_user_model().objects.get(username=query.get('allocated_to'))) if query.get('allocated_to') else tasks
    # tasks = tasks.filter(allocated_datetime=query.get('allocated_datetime')) if query.get('allocated_datetime') else tasks
    tasks = (
        tasks.filter(dcm_file__base_dcm__patient__name__icontains=query.get("name"))
        if query.get("name")
        else tasks
    )
    tasks = (
        tasks.filter(dcm_file__base_dcm__patient__sex=query.get("sex"))
        if query.get("sex")
        else tasks
    )
    if query.get('study_age_min') and query.get('study_age_max'):
        min_age = query.get('study_age_min')
        max_age = query.get('study_age_max')
        if min_age > max_age: min_age, max_age = max_age, min_age
        tasks = tasks.filter(dcm_file__base_dcm__study_age__range=(min_age, max_age))
    if query.get('bone_age_min') and query.get('bone_age_max'):
        min_age = query.get('bone_age_min')
        max_age = query.get('bone_age_max')
        if min_age > max_age: min_age, max_age = max_age, min_age
        tasks = tasks.filter(bone_age__range=(min_age, max_age))
    # tasks = tasks.filter(study_date=query.get('study_date')) if query.get('study_date') else tasks

    # TODO: 排序结果
    tasks = tasks.order_by("-allocated_datetime")

    # 查询内容分页
    current_page_number = int(query.get("page", 1))
    pages = Paginator(tasks, 15)
    page_numbers = pages.get_elided_page_range(current_page_number)
    tasks = pages.page(current_page_number)
    
    # filter用参数
    admins = get_user_model().objects.filter(is_active=True).exclude(is_staff=False)
    evaluators = get_user_model().objects.filter(is_active=True).exclude(is_staff=True)

    context = {
        "query_str": None,
        "tasks": tasks,
        "current_page_number" : current_page_number,
        "page_numbers": page_numbers,
        "has_previos": tasks.has_previous(),
        "has_next": tasks.has_next(),
        'admins' : admins,
        'evaluators' : evaluators,
    }

    # 单独取出filter相关的查询参数
    query_params = request.GET.dict()
    query_params.pop('page', None)
    context['query_str'] = "&".join([f"{key}={value}" for key, value in query_params.items()])

    return render(request, "BoneAge/library/library.html", context)


# 根据ID跳转任务、患者、影像（没做）页面
def navigator(request):
    try:
        url = {
            "task": lambda id: reverse("BoneAge_evaluator", args=(Task.objects.get(id=id).id,)),
            "patient": lambda id: reverse(
                "PatientManagement_profile", args=(Patient.objects.get(Patient_ID=id).id,)
            ) + "?info_tab=BoneAge",
            # dicom
        }[request.POST.get("type")](request.POST.get("id"))
    except ObjectDoesNotExist as e: return JsonResponse({"message": "找不到指定对象！\n" + str(e)}, status=404)
    except Exception as e: return JsonResponse({"message": "内部代码错误！\n" + str(e)}, status=500)
    return JsonResponse({"message": "跳转成功！", "url": url})
