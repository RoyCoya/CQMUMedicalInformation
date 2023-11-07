from django.urls import path
from . import views

pages = [
	# 医生主页（未完成任务）
	path('page/<int:page_number>/', views.index, name='BoneAge_index'),
	# 医生主页（已完成任务）
	path('finished/page/<int:page_number>/', views.finished_tasks, name='BoneAge_finished_tasks'),
	# 管理员主页
	path('admin/', views.admin, name='BoneAge_admin'),
	# 评分器
	path('evaluator/<int:task_id>/', views.evaluator, name='BoneAge_evaluator'),
	# 骨龄记录库
	path('library/', views.library, name='BoneAge_library'),
]

apis = [
	# 个人偏好
	path('preference/shortcut/', views.api_preference_switch_shortcut, name='api_BoneAge_preference_switch_shortcut'),
	path('preference/standard/', views.api_preference_switch_standard, name='api_BoneAge_preference_switch_standard'),
	path('preference/defaultbone/', views.api_preference_switch_default_bone, name='api_BoneAge_preference_switch_default_bone'),
	# 评分器
	path('evaluator/offset/save/', views.api_save_image_offset, name='api_BoneAge_save_image_offset'),
	path('evaluator/bone_detail/save/', views.api_modify_bone_detail, name='api_BoneAge_modify_bone_detail'),
	path('evaluator/bone_postion/save/', views.api_modify_bone_position, name='api_BoneAge_modify_bone_position'),
	path('evaluator/bone_age/save/', views.api_modify_bone_age, name='api_BoneAge_modify_bone_age'),
	path('evaluator/task/finish/', views.api_finish_task, name='api_BoneAge_finish_task'),
	path('evaluator/task/mark/', views.api_mark_task, name='api_BoneAge_mark_task'),
	# 骨龄记录库
	path('admin/dicom/upload/', views.api_upload_dcm, name='api_BoneAge_upload_dcm'),
	# 管理员后台
	path('admin/tasks/allocate/', views.api_allocate_tasks, name='api_BoneAge_allocate_tasks'),
    path('admin/tasks/delete/',views.api_delete_tasks,name='api_BoneAge_delete_tasks'),
	# TODO: 随机分配功能，单度开个功能框出来（选择标准、复选框用户后随机分配）
	path('admin/export_bone_data/', views.api_export_bone_data, name='api_BoneAge_export_bone_data'),
]

urlpatterns = pages + apis