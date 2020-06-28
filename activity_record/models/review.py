from django.db import models

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
