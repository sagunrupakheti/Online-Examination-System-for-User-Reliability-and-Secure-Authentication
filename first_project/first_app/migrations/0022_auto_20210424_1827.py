# Generated by Django 3.1.6 on 2021-04-24 12:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0021_auto_20210424_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examination',
            name='exactTimeStart',
            field=models.TimeField(default=datetime.time(18, 27, 54, 904420)),
        ),
    ]
