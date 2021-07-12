# Generated by Django 3.1.6 on 2021-04-24 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0019_auto_20210424_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='examination',
            name='exam_end_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='examination',
            name='exactTimeStart',
            field=models.TimeField(default=datetime.time(18, 26, 37, 14099)),
        ),
    ]