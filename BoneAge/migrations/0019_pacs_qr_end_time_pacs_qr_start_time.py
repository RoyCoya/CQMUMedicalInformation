# Generated by Django 4.0.6 on 2023-07-28 14:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0018_pacs_qr_running'),
    ]

    operations = [
        migrations.AddField(
            model_name='pacs_qr',
            name='end_time',
            field=models.TimeField(default=datetime.time(23, 59, 59), verbose_name='每日结束时间'),
        ),
        migrations.AddField(
            model_name='pacs_qr',
            name='start_time',
            field=models.TimeField(default=datetime.time(6, 0), verbose_name='每日启动时间'),
        ),
    ]
