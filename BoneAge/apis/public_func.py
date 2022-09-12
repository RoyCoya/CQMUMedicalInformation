import numpy as np

from BoneAge.models import Preference

# 登录检查
def login_check(request):
    user = request.user
    if not user.is_authenticated : return True
    else : return False

# 加载用户偏好设置
def load_preference(request):
    user = request.user
    preference = None
    try: preference = Preference.objects.get(user=user)
    except: preference = Preference.objects.create(user=user)
    return preference