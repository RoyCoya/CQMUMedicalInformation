from django.conf import settings
from django.http import *
from django.shortcuts import redirect

from BoneAge.apis.public_func import login_check
from BoneAge.models import Preference

# 切换快捷键开启状态
def api_preference_switch_shortcut(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    preference = Preference.objects.get(user=user)
    
    preference.shortcut = request.POST['shortcut'].title()
    preference.save()

    return HttpResponse("切换快捷键开启状态成功")

# 切换个人中心的骨骼评测标准
def api_preference_switch_standard(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    preference = Preference.objects.get(user=user)

    preference.standard = request.POST['standard']
    preference.save()
    return HttpResponse("切换默认标准成功") 

# 切换进入评分器时的默认骨骼
def api_preference_switch_default_bone(request):
    if login_check(request): return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    preference = Preference.objects.get(user=user)
    
    preference.default_bone = request.POST['default_bone']
    preference.save()

    return HttpResponse("切换默认骨骼成功")