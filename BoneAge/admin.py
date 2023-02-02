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
class admin_task(admin.ModelAdmin):
    list_display = [
        'id',
        'dcm_file',
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
admin.site.register(Task, admin_task)
admin.site.register(BoneDetail)
admin.site.register(Preference, admin_preference)