# Generated by Django 5.0.2 on 2024-02-29 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0007_alter_activitymember_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitymember',
            name='status',
            field=models.SmallIntegerField(choices=[(-1, '참가대기'), (0, '취소'), (1, '참가중')], default=0),
        ),
    ]
