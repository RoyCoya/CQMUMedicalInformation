from BoneAge.pages import index as page_index, evaluator as page_evaluator, library as page_library
from BoneAge.apis import settings as api_settings, evaluation as api_evaluation, task as api_task, admin as api_admin, superuser as api_superuser

'''
界面
'''
# 主页
def index(request, page_number): return page_index.index(request, page_number)
def finished_tasks(request, page_number): return page_index.finished_tasks(request, page_number)
def admin(request): return page_index.admin(request)
# dcm库
def library(request): return page_library.library(request)
# 评分器
def evaluator(request, task_id): return page_evaluator.evaluator(request,task_id)

'''
接口
'''
# 个人设置
def api_preference_switch_shortcut(request): return api_settings.api_preference_switch_shortcut(request)
def api_preference_switch_standard(request): return api_settings.api_preference_switch_standard(request)
def api_preference_switch_default_bone(request): return api_settings.api_preference_switch_default_bone(request)
# 评测内容修改（图片、骨龄数据）
def api_save_image_offset(request): return api_evaluation.api_save_image_offset(request)
def api_modify_bone_detail(request): return api_evaluation.api_modify_bone_detail(request)
def api_modify_bone_position(request): return api_evaluation.api_modify_bone_position(request)
def api_modify_bone_age(request): return api_evaluation.api_modify_bone_age(request)
# 任务处理
def api_finish_task(request): return api_task.api_finish_task(request)
def api_mark_task(request): return api_task.api_mark_task(request)
# 管理员操作
def api_upload_dcm(request): return api_admin.api_upload_dcm(request)
def api_allocate_tasks(request): return api_admin.api_allocate_tasks(request)
def api_delete_tasks(request): return api_admin.api_delete_tasks(request)
# def api_allocate_tasks_random(request): return api_admin.api_allocate_tasks_random(request)
# 超级管理员操作
def api_export_bone_data(request): return api_superuser.api_export_bone_data(request)