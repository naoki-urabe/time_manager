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
import re
from activity_record.modules import module
from django.contrib.auth.mixins import LoginRequiredMixin

class ActivityLogView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_active_logs = module.get_all_active_logs()
        context = {
                'all_active_logs':all_active_logs
            }
        return render(request, 'show_logs.html',context)