# Generated by Django 4.2.4 on 2023-12-14 18:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("BoneAge", "0037_alter_preference_standard"),
    ]

    operations = [
        migrations.AddField(
            model_name="preference",
            name="bone_age_copy_format_chn",
            field=models.CharField(
                default="骨龄（左手）：约{age}岁。", max_length=1000, verbose_name="骨龄复制格式（CHN）"
            ),
        ),
        migrations.AddField(
            model_name="preference",
            name="bone_age_copy_format_rus",
            field=models.CharField(
                default="骨龄（左手）：约{age}岁。", max_length=1000, verbose_name="骨龄复制格式（RUS）"
            ),
        ),
        migrations.AddField(
            model_name="preference",
            name="grade_copy_format_chn",
            field=models.CharField(
                default="按CHN法测算，左手、腕骨发育成熟度评分为{grade}分。",
                max_length=1000,
                verbose_name="分数复制格式（CHN）",
            ),
        ),
        migrations.AddField(
            model_name="preference",
            name="grade_copy_format_rus",
            field=models.CharField(
                default="按RUS-CHN法测算，左手、腕骨发育成熟度评分为{grade}分。",
                max_length=1000,
                verbose_name="分数复制格式（RUS）",
            ),
        ),
    ]
