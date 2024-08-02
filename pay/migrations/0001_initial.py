# Generated by Django 5.0.2 on 2024-06-26 14:54

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("member", "0002_adminaccount_memberdeletereason_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PayCancel",
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
                ("pay_cancel_reason", models.TextField()),
            ],
            options={
                "db_table": "tbl_pay_cancel",
            },
        ),
        migrations.CreateModel(
            name="Pay",
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
                ("price", models.IntegerField(default=20000)),
                ("receipt_id", models.TextField(null=True)),
                ("status", models.BooleanField(default=1)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="member.member"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_pay",
            },
        ),
    ]