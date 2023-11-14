from django.core.management.base import BaseCommand

from BoneAge.apis.standard import GetBoneAge
from BoneAge.models import BoneDetail, Task
class Command(BaseCommand):
    help = "根据当前的计算方式重新结算所有数据的骨龄"

    def handle(self, *args, **options):
        rectified_count = 0
        tasks = Task.objects.all()
        for i, task in enumerate(tasks):
            bones = BoneDetail.objects.filter(task=task)
            self.stdout.write('扫描 %d/%d, id: %s' % (i+1, tasks.count(), task.id))
            is_any_bone_error = sum(1 for bone in bones if bone.error != 0)
            if is_any_bone_error:
                print('存在错误的骨骼数据，跳过')
                continue
            bone_age = GetBoneAge(
                standard=task.standard,
                sex = task.dcm_file.base_dcm.patient.sex,
                bones = bones
            )
            if not bone_age:
                print('骨龄计算出错，跳过')
                continue
            origin_age = task.bone_age
            task.bone_age = bone_age
            print('原骨龄%s，更新为%s' % (str(origin_age), str(bone_age)))
            rectified_count += 1
            task.save()

        self.stdout.write(
            self.style.SUCCESS('错误骨龄校正成功，共修改 %s 条' % rectified_count )
        )