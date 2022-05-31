# Generated by Django 4.0.3 on 2022-05-31 02:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('Patient_Id', models.CharField(max_length=64, unique=True, verbose_name='Dicom Patient ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('sex', models.CharField(choices=[('Male', '男'), ('Female', '女')], max_length=6, verbose_name='性别')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='启用')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('modify_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patient_modifier', to=settings.AUTH_USER_MODEL, verbose_name='最后修改者')),
            ],
            options={
                'verbose_name': '患者',
                'verbose_name_plural': '患者',
            },
        ),
        migrations.CreateModel(
            name='DicomFile',
            fields=[
                ('dcm', models.FileField(upload_to='BoneAge/DicomFiles/%Y/%m/', verbose_name='dcm源文件')),
                ('dcm_to_image', models.ImageField(blank=True, null=True, upload_to='BoneAge/DicomFiles/%Y/%m/', verbose_name='dcm转图像')),
                ('error', models.IntegerField(choices=[(0, '已解析'), (202, '未初始化解析'), (403, '识别为非手骨图'), (415, '无法解析为图像')], default=202, verbose_name='错误类型')),
                ('SOP_Instance_UID', models.CharField(blank=True, max_length=64, null=True, verbose_name='SOP Instance UID')),
                ('Study_Date', models.DateField(blank=True, null=True, verbose_name='Study Date')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dicomfile_creater', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('modify_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dicomfile_modifier', to=settings.AUTH_USER_MODEL, verbose_name='最后修改者')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='BoneAge.patient', verbose_name='所属患者')),
            ],
            options={
                'verbose_name': 'Dicom文件',
                'verbose_name_plural': 'Dicom文件',
            },
        ),
        migrations.CreateModel(
            name='BoneAge',
            fields=[
                ('bone_age', models.FloatField(default=-1.0, verbose_name='骨龄')),
                ('closed', models.BooleanField(default=False, verbose_name='已完成')),
                ('remarks', models.TextField(blank=True, max_length=300, null=True, verbose_name='备注')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('allocated_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bone_age_allocated_to', to=settings.AUTH_USER_MODEL, verbose_name='任务分配给')),
                ('dcm_file', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BoneAge.dicomfile', verbose_name='对应dcm')),
                ('modify_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='grade_modifier', to=settings.AUTH_USER_MODEL, verbose_name='最后修改者')),
            ],
            options={
                'verbose_name': '骨龄判断结果',
                'verbose_name_plural': '骨龄判断结果',
            },
        ),
        migrations.CreateModel(
            name='BoneDetail',
            fields=[
                ('name', models.CharField(choices=[('Radius', '桡骨'), ('Ulna', '尺骨'), ('First Metacarpal', '第一掌骨'), ('First Proximal Phalange', '第一近节指骨'), ('First Distal Phalange', '第一远节指骨'), ('Third Metacarpal', '第三掌骨'), ('Third Proximal Phalange', '第三近节指骨'), ('Third Middle Phalange', '第三中节指骨'), ('Third Distal Phalange', '第三远节指骨'), ('Fifth Metacarpal', '第五掌骨'), ('Fifth Proximal Phalange', '第五近节指骨'), ('Fifth Middle Phalange', '第五中节指骨'), ('Fifth Distal Phalange', '第五远节指骨')], max_length=23, verbose_name='骨名')),
                ('level', models.IntegerField(choices=[(-1, '未评级'), (0, '0级'), (1, '1级'), (2, '2级'), (3, '3级'), (4, '4级'), (5, '5级'), (6, '6级'), (7, '7级'), (8, '8级'), (9, '9级'), (10, '10级'), (11, '11级'), (12, '12级'), (13, '13级'), (14, '14级')], default=-1, verbose_name='RUS-CHN 14阶评级')),
                ('error', models.IntegerField(choices=[(0, '正常'), (202, '未初始化解析'), (404, '无法定位')], default=202, verbose_name='定位状态')),
                ('center_x', models.FloatField(default=-1, verbose_name='中心点x')),
                ('center_y', models.FloatField(default=-1, verbose_name='中心点y')),
                ('width', models.FloatField(default=-1, verbose_name='宽度')),
                ('height', models.FloatField(default=-1, verbose_name='高度')),
                ('remarks', models.TextField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('bone_age_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bone_age_instance', to='BoneAge.boneage', verbose_name='所属骨龄记录')),
                ('modify_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bone_modifier', to=settings.AUTH_USER_MODEL, verbose_name='最后修改者')),
            ],
            options={
                'verbose_name': '骨骼具体数据',
                'verbose_name_plural': '骨骼具体数据',
                'unique_together': {('bone_age_instance', 'name')},
            },
        ),
    ]