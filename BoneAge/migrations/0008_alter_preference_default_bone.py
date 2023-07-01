# Generated by Django 4.0.6 on 2023-02-15 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0007_alter_dicomfile_error'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='default_bone',
            field=models.CharField(choices=[('radius', '桡骨'), ('ulna', '尺骨'), ('first-metacarpal', '第一掌骨'), ('third-metacarpal', '第三掌骨'), ('fifth-metacarpal', '第五掌骨'), ('first-proximal-phalange', '第一近节指骨'), ('third-proximal-phalange', '第三近节指骨'), ('fifth-proximal-phalange', '第五近节指骨'), ('third-middle-phalange', '第三中节指骨'), ('fifth-middle-phalange', '第五中节指骨'), ('first-distal-phalange', '第一远节指骨'), ('third-distal-phalange', '第三远节指骨'), ('fifth-distal-phalange', '第五远节指骨')], default='radius', max_length=100, verbose_name='默认骨骼'),
        ),
    ]