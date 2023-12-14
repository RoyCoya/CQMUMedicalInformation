from django.contrib import admin

from .models import *

class admin_dicomfile(admin.ModelAdmin):
    raw_id_fields = (
        'base_dcm',
    )
    list_display = [
        'id',
        'base_dcm',
        'error',
        'modify_user',
        'modify_date',
    ]
admin.site.register(DicomFile, admin_dicomfile)

class admin_task(admin.ModelAdmin):
    raw_id_fields = (
        'dcm_file',
    )
    list_display = [
        'id',
        'status',
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
    raw_id_fields = (
        'task',
    )
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
        'chn_default_bone',
        'rus_default_bone',
    ]
admin.site.register(Preference, admin_preference)

class admin_PACS_QR(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'base_PACS',
        'start_time',
        'end_time',
        'interval',
        'confidence',
        'allocate_to',
    ]
admin.site.register(PACS_QR, admin_PACS_QR)

class admin_PACS_QR_Log(admin.ModelAdmin):
    list_display = [
        'id',
        'pacs_qr',
        'schedule',
        'StudyDate',
        'StudyTime',
        'migrated',
    ]
admin.site.register(PACS_QR_Log, admin_PACS_QR_Log)