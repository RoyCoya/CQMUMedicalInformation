# Generated by Django 4.0.6 on 2023-07-21 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DICOMManagement', '0004_alter_dicomfile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacs',
            name='name',
            field=models.CharField(max_length=50, verbose_name='远程服务器名称'),
        ),
    ]