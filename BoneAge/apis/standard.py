import json
import os

from django.conf import settings

CHN = None
RUS = None

public_static_path = settings.STATICFILES_DIRS[0]
CHN_path = os.path.join(public_static_path, 'standard', 'BoneAge', 'CHN.json')
RUS_path = os.path.join(public_static_path, 'standard', 'BoneAge', 'RUS.json')

with open(CHN_path, 'r') as f: CHN = json.load(f)
with open(RUS_path, 'r') as f: RUS = json.load(f)

def GetJSON(standard):
    return {
        'CHN' : CHN,
        'RUS' : RUS,
    }[standard]

def GetBoneName(standard):
    return GetJSON(standard)['BoneName']

def GetBoneAge(standard, sex, bones):
    grade = 0
    standard_details = GetJSON(standard)
    if sex not in ('Male','Female'): return None

    Level_Grade = standard_details['Level_Grade'][sex]
    Grade_Age = standard_details['Grade_Age'][sex]
    
    try:
        for bone in bones: 
            bone_name = "-".join(str(bone.name).lower().split())
            grade += Level_Grade[bone_name][str(bone.assessment)]
        return next((interval['score'] for interval in Grade_Age if interval['min'] <= grade <= interval['max']), -1)
    except: return None