# Generated by Django 3.1.6 on 2021-04-23 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0011_auto_20210423_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examination',
            name='exactTimeStart',
            field=models.TimeField(default=datetime.time(13, 38, 9, 658790)),
        ),
    ]
