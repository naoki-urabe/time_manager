# Generated by Django 3.0.4 on 2020-03-27 13:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=50, verbose_name='タスク名')),
                ('begin_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('today', models.DateTimeField(default=datetime.datetime(2020, 3, 27, 13, 54, 58, 155765, tzinfo=utc))),
                ('today_jst', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('active_type', models.CharField(max_length=10, verbose_name='タスク名')),
            ],
        ),
    ]
