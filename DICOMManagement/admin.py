from django.contrib import admin

from .models import *

admin.site.register(DicomFile)
admin.site.register(PACS)