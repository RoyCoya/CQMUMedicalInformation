from django.urls import path

from . import views

pages = [
    # 患者个人资料
	path('patient/<int:patient_id>/profile/', views.profile, name='PatientManagement_profile'),
]

apis = [
    # 查询患者是否存在并返回其资料url
	path('patient/query/', views.api_query, name="PatientManagement_query"),
]

urlpatterns = pages + apis