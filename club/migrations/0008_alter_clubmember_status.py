# Generated by Django 5.0.2 on 2024-02-29 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0007_alter_clubmember_status_clubpost_clubpostreply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubmember',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '탈퇴'), (-1, '가입대기'), (1, '가입중')], default=-1),
        ),
    ]