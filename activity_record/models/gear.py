from django.db import models

class Gear(models.Model):
    subject_id = models.CharField(null=True, max_length=20)
    #subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    gear = models.fields.IntegerField(null=True)
    latest_ver = models.fields.IntegerField(null=True)
