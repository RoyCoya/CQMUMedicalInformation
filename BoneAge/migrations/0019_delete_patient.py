# Generated by Django 4.0.6 on 2022-08-22 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0018_remove_dicomfile_sop_instance_uid_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Patient',
        ),
    ]
