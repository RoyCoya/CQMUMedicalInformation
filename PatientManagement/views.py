from PatientManagement.pages import profile as page_profile
from PatientManagement.apis import query as api_query

'''
界面
'''
# 患者个人资料
def profile(request, patient_id): return page_profile.profile(request, patient_id)

'''
接口
'''
# 患者查询
def query(request): return api_query.query(request)