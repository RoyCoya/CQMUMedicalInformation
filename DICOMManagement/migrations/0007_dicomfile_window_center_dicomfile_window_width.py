# Generated by Django 4.2.1 on 2023-08-29 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DICOMManagement', '0006_alter_pacs_options_remove_pacs_config_path_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicomfile',
            name='Window_Center',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Window Center'),
        ),
        migrations.AddField(
            model_name='dicomfile',
            name='Window_Width',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Window Width'),
        ),
    ]
