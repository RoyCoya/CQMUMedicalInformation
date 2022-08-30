# Generated by Django 4.0.6 on 2022-08-22 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DICOMManagement', '0002_alter_dicomfile_sop_instance_uid'),
        ('BoneAge', '0019_delete_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicomfile',
            name='base_dcm',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='BoneAge_DicomFile_base', to='DICOMManagement.dicomfile', verbose_name='DICOM信息基类'),
        ),
    ]
