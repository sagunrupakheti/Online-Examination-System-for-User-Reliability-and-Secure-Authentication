# Generated by Django 3.1.6 on 2021-04-24 06:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0018_auto_20210423_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examination',
            name='exactTimeStart',
            field=models.TimeField(default=datetime.time(12, 37, 25, 984397)),
        ),
        migrations.CreateModel(
            name='ExamAttendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('exam_status', models.CharField(max_length=255)),
                ('exam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_app.examination')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_app.userprofileinfo')),
            ],
        ),
    ]