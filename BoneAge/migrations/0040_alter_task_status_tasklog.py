# Generated by Django 4.2.4 on 2023-12-20 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("BoneAge", "0039_remove_task_marked"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("processing", "进行中"),
                    ("reported", "等待检错"),
                    ("verifying", "等待审核"),
                    ("finished", "已完成"),
                ],
                default="processing",
                max_length=10,
                verbose_name="任务状态",
            ),
        ),
        migrations.CreateModel(
            name="TaskLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "operation",
                    models.CharField(
                        choices=[
                            ("create", "新建任务"),
                            ("update", "更新内容"),
                            ("report", "提交报错审核"),
                            ("submit", "提交完成审核"),
                            ("verify", "审核通过"),
                            ("finish", "结束任务"),
                            ("delete", "删除任务"),
                        ],
                        max_length=10,
                        verbose_name="操作",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True, max_length=5000, null=True, verbose_name="附言"
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="记录时间"),
                ),
                (
                    "operator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="BoneAge_TaskLog_operator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="",
                    ),
                ),
            ],
            options={
                "verbose_name": "任务日志",
                "verbose_name_plural": "任务日志",
            },
        ),
    ]
