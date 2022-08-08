# Generated by Django 4.0.6 on 2022-08-08 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0013_preference_bone_order_rus_alter_preference_shortcut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='bone_order_RUS',
            field=models.CharField(default='Radius|Ulna|First Metacarpal|Third Metacarpal|Fifth Metacarpal|First Proximal Phalange|Third Proximal Phalange|Fifth Proximal Phalange|Third Middle Phalange|Fifth Middle Phalange|First Distal Phalange|Third Distal Phalange|Fifth Distal Phalange', max_length=500, verbose_name='RUS 骨骼排序'),
        ),
    ]