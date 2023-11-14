from django.contrib import admin

from .models import Patient

class admin_Patient(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'sex',
        'Patient_ID',
        'birthday',
    ]
admin.site.register(Patient, admin_Patient)
