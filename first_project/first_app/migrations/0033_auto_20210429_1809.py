# Generated by Django 3.1.6 on 2021-04-29 12:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0032_auto_20210429_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examination',
            name='exactTimeStart',
            field=models.TimeField(default=datetime.time(18, 9, 16, 564579)),
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_app.course')),
            ],
        ),
    ]