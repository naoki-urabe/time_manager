# Generated by Django 3.0.4 on 2020-05-09 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_record', '0006_auto_20200505_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_id', models.CharField(max_length=20, null=True)),
                ('subject', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='activerecord',
            name='memo',
            field=models.TextField(max_length=800, null=True, verbose_name='メモ'),
        ),
    ]