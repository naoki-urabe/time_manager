from django.shortcuts import render, redirect
from django.views import View
from activity_record.models.active_record import ActiveRecord
from activity_record.models.gear import Gear
from activity_record.models.kuji_log import KujiLog
from activity_record.models.review import Review
from activity_record.models.subject import Subject
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import localtime
import datetime
from time import mktime
from activity_record.forms import ActiveRecordFormSet
from activity_record.forms import ActiveRecordForm
from activity_record.forms import SubjectFormSet
from activity_record.forms import GearFormSet
from activity_record.forms import ReviewFormSet
import re
from activity_record.modules import module

class SubjectLogView(View):
    def get(self, request, *args, **kwargs):
        subject_logs = None
        context = {
            'subject_logs':subject_logs
        }
        return render(request, 'subject_log.html',context)
    def post(self, request, *args, **kwargs):
        subject = request.POST['subject']
        subject_logs = ActiveRecord.objects.filter(task=subject).order_by('-today')
        context = {
            'subject_logs':subject_logs
        }
        return render(request, 'subject_log.html',context)