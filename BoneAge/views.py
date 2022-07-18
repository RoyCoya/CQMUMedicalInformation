from BoneAge.api import api
from BoneAge.pages import page

# TODO:把几个返回的success改成json格式，返回错误代码
# TODO:规定只能分配任务的人可以改该任务的内容

'''
界面，与 ./pages/pages.py中的页面对应
'''
#个人主页
def index(request, page_number):
    return page.index(request, page_number)

# dicom库
def dicom_library(request):
    return page.dicom_library(request)

# dicom库后台
def dicom_library_admin(request):
    return page.dicom_library_admin(request)

# 评分器
def evaluator(request, bone_age_id):
    return page.evaluator(request,bone_age_id)

'''
接口，与 ./api/api.py中的接口对应
'''
# 修改图像亮度、对比度偏移量
def api_save_image_offset(request):
    return api.api_save_image_offset(request)

# 修改骨骼评分评级等详细信息
def api_modify_bone_detail(request):
    return api.api_modify_bone_detail(request)

# 修改骨骼定位
def api_modify_bone_position(request):
    return api.api_modify_bone_position(request)

# 修改骨龄
def api_modify_bone_age(request):
    return api.api_modify_bone_age(request)

# 完成任务
def api_finish_task(request):
    return api.api_finish_task(request)

# 上传dcm
def api_upload_dcm(request):
    return api.api_upload_dcm(request)

# 解析数据库中未初始化（转png、骨骼定位）的dcm
def api_analyze_dcm(request):
    return api.api_analyze_dcm(request)

# 分配指定数量的任务给指定用户
def api_allocate_tasks(request):
    return api.api_allocate_tasks(request)

# 平均分配任务给所有用户
def api_allocate_tasks_random(request):
    return api.api_allocate_tasks_random(request)