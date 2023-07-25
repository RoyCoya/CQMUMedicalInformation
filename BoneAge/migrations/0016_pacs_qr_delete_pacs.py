# Generated by Django 4.0.6 on 2023-07-25 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DICOMManagement', '0006_alter_pacs_options_remove_pacs_config_path_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BoneAge', '0015_alter_dicomfile_options_alter_pacs_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='PACS_QR',
            fields=[
                ('name', models.CharField(max_length=50, verbose_name='配置名')),
                ('query', models.CharField(max_length=1000, verbose_name='影像筛选query')),
                ('interval', models.PositiveIntegerField(verbose_name='影像抓取间隔（分钟）')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('modify_date_time', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('create_date_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('base_PACS', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DICOMManagement.pacs', verbose_name='PACS基类')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='BoneAge_PACS_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('modify_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='BoneAge_PACS_modifier', to=settings.AUTH_USER_MODEL, verbose_name='最后修改者')),
            ],
            options={
                'verbose_name': 'PACS配置信息',
                'verbose_name_plural': 'PACS配置信息',
            },
        ),
        migrations.DeleteModel(
            name='PACS',
        ),
    ]
