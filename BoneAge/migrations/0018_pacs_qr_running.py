# Generated by Django 4.0.6 on 2023-07-25 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoneAge', '0017_pacs_qr_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='pacs_qr',
            name='running',
            field=models.BooleanField(default=False, verbose_name='启用'),
        ),
    ]
