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

class KujiLogView(View):
    def get(self, request, *args, **kwargs):
        latest_kuji_log = KujiLog.objects.all().order_by('-today').first()
        candidate = Gear.objects.filter(gear=latest_kuji_log.gear_log,latest_ver=0)
        kuji_log = KujiLog.objects.all().order_by('-today')
        context = {
                'candidate': candidate,
                'kuji_log':kuji_log
            }
        return render(request, 'kuji_log.html',context)