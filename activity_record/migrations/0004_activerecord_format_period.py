# Generated by Django 3.0.4 on 2020-04-28 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_record', '0003_activerecord_today_jst_str'),
    ]

    operations = [
        migrations.AddField(
            model_name='activerecord',
            name='format_period',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
