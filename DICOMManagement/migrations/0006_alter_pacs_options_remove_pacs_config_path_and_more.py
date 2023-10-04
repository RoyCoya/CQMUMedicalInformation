# Generated by Django 4.0.6 on 2023-07-25 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DICOMManagement', '0005_alter_pacs_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pacs',
            options={'verbose_name': '远程PACS', 'verbose_name_plural': '远程PACS'},
        ),
        migrations.RemoveField(
            model_name='pacs',
            name='config_path',
        ),
        migrations.RemoveField(
            model_name='pacs',
            name='local_AET',
        ),
        migrations.RemoveField(
            model_name='pacs',
            name='local_http_port',
        ),
        migrations.RemoveField(
            model_name='pacs',
            name='local_ip',
        ),
        migrations.RemoveField(
            model_name='pacs',
            name='local_port',
        ),
        migrations.AlterField(
            model_name='pacs',
            name='name',
            field=models.CharField(max_length=50, verbose_name='服务器名称'),
        ),
        migrations.AlterField(
            model_name='pacs',
            name='remote_AET',
            field=models.CharField(max_length=50, verbose_name='实体名（AE title）'),
        ),
        migrations.AlterField(
            model_name='pacs',
            name='remote_ip',
            field=models.GenericIPAddressField(verbose_name='IP'),
        ),
        migrations.AlterField(
            model_name='pacs',
            name='remote_port',
            field=models.PositiveIntegerField(verbose_name='端口号'),
        ),
        migrations.CreateModel(
            name='PACS_conf',
            fields=[
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='描述')),
                ('path', models.CharField(max_length=1000, verbose_name='配置文件保存路径')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='DICOMManagement_PACS_conf_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': 'PACS配置记录',
                'verbose_name_plural': 'PACS配置记录',
            },
        ),
    ]