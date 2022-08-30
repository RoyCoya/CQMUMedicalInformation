from django.contrib import admin
from .models import *

# TODO:找时间优化下。编码参考里有资料
class admin_dicomfile(admin.ModelAdmin):
    list_display = [
        'id',
        'base_dcm',
        'error',
        'modify_user',
        'modify_date',
    ]
class admin_boneage(admin.ModelAdmin):
    list_display = [
        'id',
        'dcm_file',
		'bone_age',
        'allocated_to',
        'closed',
        'closed_date',
        'modify_date',
    ]
class admin_preference(admin.ModelAdmin):
    list_display = [
        'user',
        'shortcut',
		'standard',
        'default_bone',
    ]
admin.site.register(DicomFile, admin_dicomfile)
admin.site.register(BoneAge, admin_boneage)
admin.site.register(BoneDetail)
admin.site.register(Preference, admin_preference)