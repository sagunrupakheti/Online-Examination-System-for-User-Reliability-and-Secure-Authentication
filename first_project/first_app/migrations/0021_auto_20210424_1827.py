# Generated by Django 3.1.6 on 2021-04-24 12:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0020_auto_20210424_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examination',
            name='exactTimeStart',
            field=models.TimeField(default=datetime.time(18, 27, 46, 602735)),
        ),
        migrations.AlterField(
            model_name='examination',
            name='exam_end_time',
            field=models.DateTimeField(blank=True),
        ),
    ]
