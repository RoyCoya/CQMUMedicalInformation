from django import template
import math
import time

register = template.Library()

@register.filter(name='time_period_alert')
def convert_time_to_period(value):
    #根据当前时间转为早中晚
    time_hour = time.localtime().tm_hour
    if time_hour > 0 and time_hour <= 6:
        return "凌晨好，" + value + "医生"
    elif time_hour > 6 and time_hour <= 12:
        return "早上好，" + value + "医生"
    elif time_hour > 12 and time_hour <= 18:
        return "下午好，" + value + "医生"
    elif time_hour >18 and time_hour <= 24:
        return "晚上好，" + value + "医生"

# 根据dicom计算检查时的实际年龄
@register.filter(name='get_dcm_age')
def get_dcm_age(birthday, study_date):
    return (study_date - birthday).days / 365

# get转义符
@register.filter(name='transfercharacter_get_url')
def transfercharacter_get_url(get_params):
    get_params = get_params.replace('+', r'%2B')
    get_params = get_params.replace('=', r'%3D')
    get_params = get_params.replace('&', r'%26')
    get_params = get_params.replace('#', r'%23')
    get_params = get_params.replace('%', r'%25')
    get_params = get_params.replace('?', r'%3F')
    get_params = get_params.replace('/', r'%2F')
    get_params = get_params.replace(' ', r'%20')
    return get_params

# 值相减
@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

# 取绝对值
@register.filter(name='abs')
def abs(value):
    return math.fabs(value)