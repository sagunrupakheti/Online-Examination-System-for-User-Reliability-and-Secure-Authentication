# Generated by Django 3.1.6 on 2021-04-26 17:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0025_auto_20210426_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examination',
            name='exactTimeStart',
            field=models.TimeField(default=datetime.time(23, 12, 36, 51969)),
        ),
    ]
