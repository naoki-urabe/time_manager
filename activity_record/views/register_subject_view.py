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

class RegisterSubjectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        formset = SubjectFormSet()
        context = {
            'formset': formset
        }
        return render(request, 'register_subject.html',context)
    def post(self, request, *args, **kwargs):
        formset = SubjectFormSet(request.POST or None, queryset=Subject.objects.all())
        if formset.is_valid():
            instance = formset.save(commit=False)
            print(instance)
            for inst in formset.deleted_objects:
                inst.delete()
            for form in instance:
                print('-----------------------')
                print(form)
                print('-----------------------')
                form.save()
            formset = SubjectFormSet()
            context = {
                'formset': formset
            }
            return render(request, 'register_subject.html',context)
        else:
            print(formset._errors)
            context = {
                'register_msg': formset._errors,
                'formset': formset
            }
            return render(request, 'register_subject.html',context)