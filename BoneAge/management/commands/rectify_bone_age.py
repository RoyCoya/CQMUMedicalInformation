from django.core.management.base import BaseCommand

from BoneAge.apis.Standard.Converter import GetBoneAge
from BoneAge.models import BoneDetail, Task
class Command(BaseCommand):
    help = "2023-07-19 之前的系统内Task.bone_age都是默认值-1，没有经过计算，其内容都在前端。\n从07-18的commit后增加了计算，故以此脚本清洗之前尚计算的bone age。"

    def handle(self, *args, **options):
        rectified_count = 0
        tasks = Task.objects.all()
        for i, task in enumerate(tasks):
            bones = BoneDetail.objects.filter(task=task)
            self.stdout.write('scanning %d/%d' % (i+1, tasks.count()))
            is_any_bone_error = sum(1 for bone in bones if bone.error != 0)
            if not is_any_bone_error:
                bone_age = GetBoneAge(
                    standard=task.standard,
                    sex = task.dcm_file.base_dcm.patient.sex,
                    bones = bones
                )
                if not bone_age: continue
                task.bone_age = bone_age
                rectified_count += 1
                task.save()
        self.stdout.write(
            self.style.SUCCESS('错误骨龄校正成功，共修改 %s 条' % rectified_count )
        )