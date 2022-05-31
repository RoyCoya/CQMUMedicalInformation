from django.contrib import admin
from .models import Patient, DicomFile, BoneAge, BoneDetail

# TODO:找时间优化下。编码参考里有资料
class admin_patient(admin.ModelAdmin):
    actions_on_top = True
    date_hierarchy = 'modify_date'
    list_display = [
        'id',
        'Patient_Id',
		'name',
        'sex',
        'active',
        'modify_user',
    ]
    fieldsets = (
        (None, {
            'fields': ('Patient_Id', 'name', 'sex', )
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
admin.site.register(Patient, admin_patient)
admin.site.register(DicomFile, admin_dicomfile)
admin.site.register(BoneAge)
admin.site.register(BoneDetail)
