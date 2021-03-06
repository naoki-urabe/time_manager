# Generated by Django 3.0.4 on 2020-03-28 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=50, null=True, verbose_name='タスク名')),
                ('begin_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('period', models.FloatField(null=True)),
                ('today', models.DateTimeField(null=True)),
                ('today_jst', models.DateField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('active_type', models.CharField(max_length=10, null=True, verbose_name='タスク名')),
            ],
        ),
    ]
