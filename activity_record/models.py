from django.db import models
from django.utils import timezone

# Create your models here.
class ActiveRecord(models.Model):
    task = models.CharField(verbose_name='タスク名', max_length=50,null=True)
    begin_time = models.fields.DateTimeField(null=True)
    end_time = models.fields.DateTimeField(null=True)
    period = models.fields.FloatField(null=True)
    format_period = models.fields.CharField(null=True, max_length=20)
    today = models.fields.DateTimeField(null=True)
    today_jst = models.fields.DateField(null=True)
    today_jst_str = models.CharField(null=True, max_length=20)
    is_active = models.fields.BooleanField(default = True)
    active_type = models.CharField(verbose_name='タスクタイプ', max_length=10,null=True)
    memo = models.TextField(verbose_name='メモ', max_length=800,null=True)

class Subject(models.Model):
    subject_id = models.CharField(null=True, max_length=20)
    subject = models.CharField(null=True, max_length=20)

class Gear(models.Model):
    subject_id = models.CharField(null=True, max_length=20)
    #subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    gear = models.fields.IntegerField(null=True)
    latest_ver = models.fields.IntegerField(null=True)

class KujiLog(models.Model):
    gear_log = models.fields.IntegerField(null=True)
    cycle_log = models.fields.IntegerField(null=True)
    latest_ver = models.fields.IntegerField(null=True)
    today = models.fields.DateTimeField(null=True)
    #subject_id = models.CharField(null=True, max_length=20)
    subject = models.CharField(null=True, max_length=20)
    today_jst_str = models.CharField(null=True, max_length=20)
    #subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)

class Review(models.Model):
    review_id = models.CharField(null=True, max_length=6)
    subject_id =  models.CharField(null=True, max_length=20)
    summary =  models.CharField(null=True, max_length=50)
    is_online = models.fields.CharField(null=True, max_length=10)
    version = models.fields.IntegerField(null=True)
    today = models.fields.DateTimeField(null=True)
    today_date = models.fields.DateField(null=True)
    tomorrow = models.fields.DateField(null=True)
    one_week_later = models.fields.DateField(null=True)
    two_week_later = models.fields.DateField(null=True)
    one_month_later = models.fields.DateField(null=True)
