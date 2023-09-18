# Generated by Django 4.2.1 on 2023-08-27 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0021_remove_pacs_qr_delay_pacs_qr_confidence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicomfile',
            name='error',
            field=models.IntegerField(choices=[(0, '已解析'), (102, '分配中'), (202, '未初始化解析'), (403, '识别为非手骨图'), (422, '无法解析为图像')], default=202, verbose_name='错误类型'),
        ),
    ]
