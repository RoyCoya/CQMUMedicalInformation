# Generated by Django 4.2.1 on 2023-10-01 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0028_pacs_qr_standard_alter_dicomfile_error'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacs_qr_log',
            name='pacs_qr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='BoneAge.pacs_qr', verbose_name='配置'),
        ),
    ]
