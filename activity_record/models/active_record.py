from django.db import models

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
    study_amount = models.fields.IntegerField(null=True)