# Generated by Django 3.0.4 on 2020-05-10 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_record', '0008_auto_20200510_1508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kujilog',
            old_name='subject_id',
            new_name='subject',
        ),
    ]