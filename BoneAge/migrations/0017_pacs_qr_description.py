# Generated by Django 4.0.6 on 2023-07-25 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0016_pacs_qr_delete_pacs'),
    ]

    operations = [
        migrations.AddField(
            model_name='pacs_qr',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='描述'),
        ),
    ]
