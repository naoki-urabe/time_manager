# Generated by Django 3.0.4 on 2020-05-15 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_record', '0013_auto_20200515_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='today_date',
            field=models.DateField(null=True),
        ),
    ]
