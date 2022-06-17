# Generated by Django 2.2.5 on 2022-06-17 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0004_rename_patient_id_patient_patient_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicomfile',
            name='brightness',
            field=models.IntegerField(default=100, verbose_name='亮度偏量（百分数）'),
        ),
        migrations.AddField(
            model_name='dicomfile',
            name='contrast',
            field=models.IntegerField(default=100, verbose_name='对比度偏量（百分数）'),
        ),
    ]
