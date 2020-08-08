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
from django.contrib.auth.mixins import LoginRequiredMixin

class ActivityDetailView(LoginRequiredMixin, View):
    def get(self, request,today_jst_str, *args, **kwargs):
        active_histories = ActiveRecord.objects.filter(today_jst_str=today_jst_str).order_by('-today')
        print(active_histories)
        context = {
            'today_activity': active_histories,
            'today_jst_str': today_jst_str
        }
        return render(request, 'log_detail.html', context)