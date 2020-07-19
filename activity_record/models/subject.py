from django.db import models

class Subject(models.Model):
    subject_id = models.CharField(null=True, max_length=20)
    subject = models.CharField(null=True, max_length=20)
    subject_type = models.CharField(null=True, max_length=20)