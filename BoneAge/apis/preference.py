from django.conf import settings
from django.http import *
from django.contrib.auth.decorators import login_required

from BoneAge.models import Preference

# 切换快捷键开启状态
@login_required
def api_preference_switch_shortcut(request):
    user = request.user
    preference = Preference.objects.get(user=user)
    
    preference.shortcut = request.POST['shortcut'].title()
    preference.save()

    return HttpResponse("切换快捷键开启状态成功")

# 切换进入评分器时的默认骨骼
@login_required
def api_preference_switch_default_bone(request):
    user = request.user
    preference = Preference.objects.get(user=user)
    
    preference.default_bone = request.POST['default_bone']
    preference.save()

    return HttpResponse("切换默认骨骼成功")
