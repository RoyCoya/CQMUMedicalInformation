import cv2
import numpy as np

from BoneAge.apis.bone_analysis_RUS import OnnxInfer as analysis_RUS
from BoneAge.apis.bone_analysis_CHN import OnnxInfer as analysis_CHN
from django.conf import settings

def bone_detect(img_path, standard):
    model = {
        'RUS' : lambda : analysis_RUS(str(settings.STATICFILES_DIRS[0]) + 'onnx_models/BoneAge/RUS.onnx'),
        'CHN' : lambda : analysis_CHN(str(settings.STATICFILES_DIRS[0]) + 'onnx_models/BoneAge/CHN.onnx'),
    }[standard]()
    return model.do_infer(img_path)