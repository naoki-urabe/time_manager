# Generated by Django 3.0.4 on 2020-03-28 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_record', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activerecord',
            name='period',
            field=models.FloatField(null=True),
        ),
    ]
