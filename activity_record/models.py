from django.db import models
from django.utils import timezone

# Create your models here.
class ActiveRecord(models.Model):
    task = models.CharField(verbose_name='タスク名', max_length=50)
    begin_time = models.fields.DateTimeField(null=True)
    end_time = models.fields.DateTimeField(null=True)
    #period = models.fields.FloatField(null=True)
    today = models.fields.DateTimeField(default = timezone.now())
    today_jst = models.fields.DateField()
    is_active = models.fields.BooleanField(default = True)
    active_type = models.CharField(verbose_name='タスク名', max_length=10)