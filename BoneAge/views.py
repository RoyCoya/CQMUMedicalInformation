from BoneAge.pages import index, evaluator, library, admin
from BoneAge.apis import preference as api_settings, evaluation as api_evaluation, task as api_task, admin as api_admin, superuser as api_superuser

'''
界面
'''
# 主页
def page_index(request, page_number): return index.index(request, page_number)
def page_finished_tasks(request, page_number): return index.finished_tasks(request, page_number)
# 管理员
def page_admin(request): return admin.admin(request)
# dcm库
def page_library(request): return library.library(request)
def page_navigator(request): return library.navigator(request)
# 评分器
def page_evaluator(request, task_id): return evaluator.evaluator(request,task_id)

'''
接口
'''
# 个人设置
def api_preference_switch_shortcut(request): return api_settings.preference_switch_shortcut(request)
def api_preference_switch_default_bone(request): return api_settings.preference_switch_default_bone(request)
# 评测内容修改（图片、骨龄数据）
def api_save_image_offset(request): return api_evaluation.save_image_offset(request)
def api_modify_bone_detail(request): return api_evaluation.modify_bone_detail(request)
def api_modify_bone_position(request): return api_evaluation.modify_bone_position(request)
# 任务处理
def api_finish_task(request): return api_task.finish_task(request)
def api_mark_task(request): return api_task.mark_task(request)
# 管理员操作
def api_upload_dcm(request): return api_admin.upload_dcm(request)
def api_allocate_tasks(request): return api_admin.allocate_tasks(request)
def api_delete_tasks(request): return api_admin.delete_tasks(request)
# def api_allocate_tasks_random(request): return api_admin.api_allocate_tasks_random(request)
# 超级管理员操作
def api_export_bone_data(request): return api_superuser.export_bone_data(request)