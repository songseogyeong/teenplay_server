# Generated by Django 5.0.2 on 2024-06-26 14:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("member", "0002_adminaccount_memberdeletereason_and_more"),
        ("teenplay", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TeenPlayLike",
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
                ("status", models.BooleanField(default=1)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="member.member"
                    ),
                ),
                (
                    "teenplay",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="teenplay.teenplay",
                    ),
                ),
            ],
            options={
                "db_table": "tbl_teenplay_like",
            },
        ),
    ]