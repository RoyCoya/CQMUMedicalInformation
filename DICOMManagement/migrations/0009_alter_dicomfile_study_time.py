# Generated by Django 4.2.1 on 2023-09-17 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DICOMManagement', '0008_dicomfile_study_time_alter_dicomfile_study_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicomfile',
            name='Study_Time',
            field=models.TimeField(blank=True, default=None, null=True, verbose_name='Study Time'),
        ),
    ]
