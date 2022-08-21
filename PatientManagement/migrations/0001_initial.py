# Generated by Django 4.0.6 on 2022-08-20 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('Patient_ID', models.CharField(max_length=64, unique=True, verbose_name='Dicom Patient ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('sex', models.CharField(choices=[('Male', '男'), ('Female', '女')], max_length=6, verbose_name='性别')),
                ('birthday', models.DateField(verbose_name='生日')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='启用')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('modify_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patient_modifier', to=settings.AUTH_USER_MODEL, verbose_name='最后修改者')),
            ],
            options={
                'verbose_name': '患者',
                'verbose_name_plural': '患者',
            },
        ),
    ]