from PatientManagement.pages import profile as page_profile

# Create your views here.
# 患者个人资料
def profile(request, patient_id): return page_profile.profile(request, patient_id)