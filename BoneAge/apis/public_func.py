from BoneAge.models import Preference

# 加载用户偏好设置
def load_preference(request):
    user = request.user
    preference = None
    try: preference = Preference.objects.get(user=user)
    except: preference = Preference.objects.create(user=user)
    return preference