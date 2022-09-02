from django.urls import path
from . import views

urlpatterns = [
	#页面
	path('page/<int:page_number>/order/<int:order>/descend/<int:is_descend>/', views.index, name='BoneAge_index'),
	path('finished/page/<int:page_number>/order/<int:order>/descend/<int:is_descend>/', views.finished_tasks, name='BoneAge_finished_tasks'),
	path('evaluator/<int:bone_age_id>/', views.evaluator, name='BoneAge_evaluator'),
	path('dicom/library/', views.dicom_library, name='BoneAge_dicom_library'),
	path('dicom/library/admin/', views.dicom_library_admin, name='BoneAge_dicom_library_admin'),
	#接口
	path('preference/shortcut/', views.api_preference_switch_shortcut, name='api_BoneAge_preference_switch_shortcut'),
	path('preference/defaultbone/', views.api_preference_switch_default_bone, name="api_BoneAge_preference_switch_default_bone"),
	path('evaluator/offset/save/', views.api_save_image_offset, name='api_BoneAge_save_image_offset'),
	path('evaluator/bone_detail/save/', views.api_modify_bone_detail, name='api_BoneAge_modify_bone_detail'),
	path('evaluator/bone_postion/save/', views.api_modify_bone_position, name='api_BoneAge_modify_bone_position'),
	path('evaluator/bone_age/save/', views.api_modify_bone_age, name='api_BoneAge_modify_bone_age'),
	path('evaluator/task/finish/', views.api_finish_task, name='api_BoneAge_finish_task'),
	path('evaluator/task/mark/', views.api_mark_task, name='api_BoneAge_mark_task'),
	path('dicom/library/admin/dicom/upload/', views.api_upload_dcm, name='api_BoneAge_upload_dcm'),
	path('dicom/library/admin/dicom/analyze/', views.api_analyze_dcm, name='api_BoneAge_analyze_dcm'),
	path('dicom/library/admin/tasks/allocate/', views.api_allocate_tasks, name="api_BoneAge_allocate_tasks"),
	path('dicom/library/admin/tasks/allocate/random/', views.api_allocate_tasks_random, name="api_BoneAge_allocate_tasks_random"),
	path('dicom/library/admin/export_bone_data/', views.api_export_bone_data, name="api_BoneAge_export_bone_data"),
]