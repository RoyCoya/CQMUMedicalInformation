# Generated by Django 4.0.6 on 2023-02-16 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DICOMManagement', '0002_alter_dicomfile_sop_instance_uid'),
        ('BoneAge', '0010_alter_preference_default_bone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dicomfile',
            options={'verbose_name': '骨龄用dcm扩展信息', 'verbose_name_plural': '骨龄用dcm扩展信息'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': '任务', 'verbose_name_plural': '任务'},
        ),
        migrations.AlterField(
            model_name='dicomfile',
            name='base_dcm',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='BoneAge_DicomFile_base', to='DICOMManagement.dicomfile', verbose_name='dcm基类'),
        ),
    ]