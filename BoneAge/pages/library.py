from django.conf import settings
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from BoneAge.apis.public_func import login_check
from BoneAge.apis.dicom import get_study_age
from BoneAge.models import Task
from PatientManagement.models import Patient


# 所有记录
def library(request):
    if login_check(request):
        return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))
    query = request.GET

    # 筛选结果
    tasks = Task.objects.all()
    tasks = tasks.filter(status=query.get("status")) if query.get("status") else tasks
    # tasks = tasks.filter(allocator=query.get('allocator')) if query.get('allocator') else tasks
    # tasks = tasks.filter(allocatee=query.get('allocatee')) if query.get('allocatee') else tasks
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
    # tasks = tasks.filter(study_age=query.get('study_age')) if query.get('study_age') else tasks
    # tasks = tasks.filter(bone_age=query.get('bone_age')) if query.get('bone_age') else tasks
    # tasks = tasks.filter(study_date=query.get('study_date')) if query.get('study_date') else tasks

    # TODO: 排序结果
    tasks = tasks.order_by("-allocated_datetime")

    for task in tasks:
        task.study_age = get_study_age(task.dcm_file.base_dcm)

    # 查询内容分页
    current_page_number = query.get("page", 1)
    pages = Paginator(tasks, 15)
    page_numbers = pages.get_elided_page_range(current_page_number)
    tasks = pages.page(current_page_number)

    context = {
        "query_str": request.META["QUERY_STRING"],
        "tasks": tasks,
        "page_numbers": page_numbers,
        "has_previos": tasks.has_previous(),
        "has_next": tasks.has_next(),
    }
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
