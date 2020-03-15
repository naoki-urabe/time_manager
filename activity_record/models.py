from django.db import models
from django.utils import timezone

# Create your models here.
class ActiveRecord(models.Model):
    task = models.CharField(verbose_name='タスク名', max_length=50)
    begin_time = models.fields.DateTimeField(null=True)
    end_time = models.fields.DateTimeField(null=True)
    period = models.fields.DateTimeField(null=True)
    today = models.fields.DateField(default = timezone.now().date())
    is_active = models.fields.BooleanField(default = True)

class TaskRecord(models.Model):
    task = models.CharField(verbose_name='タスク名', max_length=50)
    begin_time = models.fields.DateTimeField(null=True)
    end_time = models.fields.DateTimeField(null=True)
    period = models.fields.DateTimeField(null=True)
    today = models.fields.DateField(default = timezone.now().date())
    is_active = models.fields.BooleanField(default = True)