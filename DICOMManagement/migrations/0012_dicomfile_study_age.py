# Generated by Django 4.2.4 on 2023-12-15 17:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("DICOMManagement", "0011_alter_dicomfile_dcm_alter_dicomfile_dcm_to_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="dicomfile",
            name="study_age",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=None, max_digits=4, null=True
            ),
        ),
    ]