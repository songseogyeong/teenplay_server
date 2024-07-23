# Generated by Django 5.0.2 on 2024-06-26 14:52

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("club", "0003_clubcategory_clubpostreply"),
    ]

    operations = [
        migrations.CreateModel(
            name="TeenPlay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "updated_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("teenplay_title", models.TextField()),
                ("video_path", models.ImageField(upload_to="teenplay_video/%Y/%m/%d")),
                (
                    "thumbnail_path",
                    models.ImageField(upload_to="teenplay_thumbnail/%Y/%m/%d"),
                ),
                ("status", models.BooleanField(default=1)),
                (
                    "club",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="club.club"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_teenplay",
            },
        ),
    ]
