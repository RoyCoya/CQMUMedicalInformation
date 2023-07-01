# Generated by Django 4.0.6 on 2023-02-16 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0012_alter_bonedetail_error'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonedetail',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BoneAge_BoneDetail_task', to='BoneAge.task', verbose_name='所属任务'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='bone_order_CHN',
            field=models.CharField(default='Radius|Capitate|Hamate|First Metacarpal|Third Metacarpal|Fifth Metacarpal|First Proximal Phalange|Third Proximal Phalange|Fifth Proximal Phalange|Third Middle Phalange|Fifth Middle Phalange|First Distal Phalange|Third Distal Phalange|Fifth Distal Phalange', max_length=500, verbose_name='CHN 骨骼排序'),
        ),
    ]