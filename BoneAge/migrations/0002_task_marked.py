# Generated by Django 4.0.6 on 2022-09-02 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='marked',
            field=models.BooleanField(default=False, verbose_name='收藏'),
        ),
    ]
