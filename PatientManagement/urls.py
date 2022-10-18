from django.urls import path
from . import views

urlpatterns = [
	# 患者个人资料
	path('patient/<int:patient_id>/profile/', views.profile, name='PatientManagement_profile'),
]