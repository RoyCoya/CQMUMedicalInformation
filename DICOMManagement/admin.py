from django.contrib import admin

from .models import *

class admin_DicomFile(admin.ModelAdmin):
    list_display = [
        'id',
        'patient',
        'SOP_Instance_UID',
        'create_date',
        'create_user',
        'dcm',
        'dcm_to_image',
    ]
admin.site.register(DicomFile, admin_DicomFile)
admin.site.register(PACS)