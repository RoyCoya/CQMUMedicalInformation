from PatientManagement.pages import profile as page_profile
from PatientManagement.apis import query

'''
界面
'''
# 患者个人资料
def profile(request, patient_id): return page_profile.profile(request, patient_id)

'''
接口
'''
# 患者查询
def api_query(request): return query.query(request)