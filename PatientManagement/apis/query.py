import json
import time

from django.urls import reverse
from django.http import *

from PatientManagement.models import Patient

def query(request):
    code = 202
    msg = "查询开始"
    patient_id = None
    info_tab = None
    try: 
        patient_id = request.GET['patient_id']
        info_tab = request.GET['type']
    except Exception as e: return HttpResponseBadRequest(e)

    try:
        patient_id = Patient.objects.get(Patient_ID=patient_id).id
        code = 200
    except: code = 404

    msg = {
            200 : lambda : "查询成功",
            404 : lambda : "该患者未录入系统",
    }[code]()

    response = {
        "code" : code,
        "msg" : msg,
        "time" : time.time(),
        "data" : {
            "url" : "http://172.16.29.15:8000"+ reverse("PatientManagement_profile", args=(int(patient_id),)) + '?info_tab=' + info_tab,
        },
    }
    return HttpResponse(json.dumps(response), content_type="application/json")