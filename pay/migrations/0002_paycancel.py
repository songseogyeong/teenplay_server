# Generated by Django 5.0.2 on 2024-03-11 13:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayCancel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('pay_cancel_reason', models.TextField()),
            ],
            options={
                'db_table': 'tbl_pay_cancle',
            },
        ),
    ]
