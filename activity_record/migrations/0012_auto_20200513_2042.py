# Generated by Django 3.0.4 on 2020-05-13 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_record', '0011_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='is_online',
            field=models.CharField(max_length=10, null=True),
        ),
    ]