# Generated by Django 3.0.4 on 2020-03-29 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_record', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activerecord',
            name='memo',
            field=models.CharField(max_length=100, null=True, verbose_name='メモ'),
        ),
        migrations.AlterField(
            model_name='activerecord',
            name='active_type',
            field=models.CharField(max_length=10, null=True, verbose_name='タスクタイプ'),
        ),
    ]
