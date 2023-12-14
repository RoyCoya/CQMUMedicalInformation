import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from BoneAge.models import Preference
from BoneAge.apis.public_func import load_preference

# 设置偏好
@login_required
def save(request):
    preference = load_preference(request)

    try:
        for field_name, field_value in request.POST.items():
            try:
                setattr(preference, field_name, field_value)
                preference.save()
            except AttributeError: return JsonResponse({'message': f'不存在字段 {field_name}'}, status=400)
        return JsonResponse({'message': '设置保存成功'})
    except json.JSONDecodeError: return JsonResponse({'message': f'无效的 JSON 数据\n原数据：{request.body}'}, status=400)
