from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render

from BoneAge.models import DicomFile, PACS_QR

# 管理员页面
def admin(request):
    # 数据库状态检查
    error_dcm_count = DicomFile.objects.exclude(error=0).exclude(error=102).count()
    # TODO: 根据单一或数个标准查询未分配任务的dcm
    unallocated_dcm = DicomFile.objects.annotate(dcm_tasks=Count('BoneAge_Task_affiliated_dcm')).exclude(dcm_tasks__gt=0).filter(error__in=[0,403]).filter(create_user=request.user)
    # 可用于任务分配的账号
    user_model = get_user_model()
    evaluators = user_model.objects.filter(is_active=True).exclude(is_staff=True)
    # 远程PACS
    PACS_list = PACS_QR.objects.all()

    context = {
        'unallocated_dcm' : unallocated_dcm,
        'error_dcm_count' : error_dcm_count,
        'evaluators' : evaluators,
        'PACS_list' : PACS_list,
    }
    return render(request,'BoneAge/admin/admin.html', context)