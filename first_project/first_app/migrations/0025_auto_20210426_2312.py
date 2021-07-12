# Generated by Django 3.1.6 on 2021-04-26 17:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0024_auto_20210424_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examination',
            name='exactTimeStart',
            field=models.TimeField(default=datetime.time(23, 12, 18, 69499)),
        ),
        migrations.CreateModel(
            name='SamplePicsStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_status', models.CharField(max_length=255)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_app.userprofileinfo')),
            ],
        ),
    ]
