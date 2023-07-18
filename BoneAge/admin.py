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
admin.site.register(DicomFile, admin_dicomfile)

class admin_task(admin.ModelAdmin):
    list_display = [
        'id',
        'dcm_file',
        'standard',
        'bone_age',
        'allocated_to',
        'closed',
        'closed_date',
        'modify_date',
    ]
admin.site.register(Task, admin_task)

class admin_bonedetail(admin.ModelAdmin):
    list_display = [
        'id',
        'task',
        'name',
        'assessment',
        'error',
    ]
admin.site.register(BoneDetail, admin_bonedetail)

class admin_preference(admin.ModelAdmin):
    list_display = [
        'user',
        'shortcut',
		'standard',
        'default_bone',
    ]
admin.site.register(Preference, admin_preference)