from django import template
import math
import time

register = template.Library()


# 骨骼排序转list
@register.filter(name="BoneOrder")
def BoneOrder(value: str):
    bones = value.split("|")
    bone_dict = {
        "Radius": "桡骨",
        "Ulna": "尺骨",
        "Capitate": "头状骨",
        "Hamate": "钩骨",
        "First Metacarpal": "第一掌骨",
        "Third Metacarpal": "第三掌骨",
        "Fifth Metacarpal": "第五掌骨",
        "First Proximal Phalange": "第一近节指骨",
        "Third Proximal Phalange": "第三近节指骨",
        "Fifth Proximal Phalange": "第五近节指骨",
        "Third Middle Phalange": "第三中节指骨",
        "Fifth Middle Phalange": "第五中节指骨",
        "First Distal Phalange": "第一远节指骨",
        "Third Distal Phalange": "第三远节指骨",
        "Fifth Distal Phalange": "第五远节指骨",
    }
    return {bone: bone_dict[bone] for bone in bones}.items()
