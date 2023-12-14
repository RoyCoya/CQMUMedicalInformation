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
            except: pass
        return JsonResponse({'message': '设置保存成功'})
    except Exception as e: return JsonResponse({'message': f'访问出错：{str(e)}'}, status=400)
