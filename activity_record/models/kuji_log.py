from django.db import models

class KujiLog(models.Model):
    gear_log = models.fields.IntegerField(null=True)
    cycle_log = models.fields.IntegerField(null=True)
    latest_ver = models.fields.IntegerField(null=True)
    today = models.fields.DateTimeField(null=True)
    #subject_id = models.CharField(null=True, max_length=20)
    subject = models.CharField(null=True, max_length=20)
    today_jst_str = models.CharField(null=True, max_length=20)
    #subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)