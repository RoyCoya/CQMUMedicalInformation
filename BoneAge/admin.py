from django.contrib import admin
from .models import Patient, DicomFile, BoneAge, BoneDetail

# TODO:找时间优化下。编码参考里有资料
class admin_patient(admin.ModelAdmin):
    actions_on_top = True
    date_hierarchy = 'modify_date'
    list_display = [
        'id',
        'Patient_ID',
		'name',
        'sex',
        'birthday',
        'active',
        'modify_user',
    ]
    fieldsets = (
        (None, {
            'fields': ('Patient_ID', 'name', 'sex', 'birthday' )
        }),
        ('系统信息', {
            'classes': ('collapse',),
            'fields': ('modify_user', 'active'),
        }),
    )
class admin_dicomfile(admin.ModelAdmin):
    list_display = [
        'id',
        'patient',
		'SOP_Instance_UID',
        'Study_Date',
        'error',
        'modify_user',
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
admin.site.register(Patient, admin_patient)
admin.site.register(DicomFile, admin_dicomfile)
admin.site.register(BoneAge,admin_boneage)
admin.site.register(BoneDetail)
