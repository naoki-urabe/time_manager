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

class EditLogView(LoginRequiredMixin, View):
    def get(self, request,today_jst_str, *args, **kwargs):
        formset = ActiveRecordFormSet(request.POST or None, queryset=ActiveRecord.objects.filter(today_jst_str=today_jst_str).order_by('-today'))
        context = {
            'formset':formset,
            'today_jst_str':today_jst_str
        }
        return render(request, 'edit_log.html',context)
    def post(self, request,today_jst_str, *args, **kwargs):
        formset = ActiveRecordFormSet(request.POST or None, queryset=ActiveRecord.objects.filter(today_jst_str=today_jst_str))
        if formset.is_valid():
            instance = formset.save(commit=False)
            for form in instance:
                form.today_jst_str = localtime(form.today).strftime('%Y%m%d')
                form.is_active = False
                form.period = module.timedelta_to_sec(form.end_time - form.begin_time)
                form.format_period = module.format_timedelta(form.period)
                form.save()
            formset = ActiveRecordFormSet(request.POST or None, queryset=ActiveRecord.objects.filter(today_jst_str=today_jst_str).order_by('-today'))
            context = {
                'register_msg': '登録完了',
                'formset':formset,
                'today_jst_str':today_jst_str
            }
            return render(request, 'edit_log.html',context)
        else:
            print(formset._error())
            context = {
                'register_msg': '登録失敗',
                'formset':formset,
                'today_jst_str':today_jst_str
            }
            return render(request, 'edit_log.html',context)