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

class ReviewListView(View):
    def get(self, request, *args, **kwargs):
        review_list = Review.objects.all().order_by('-today')
        context = {
                'review_list':review_list
            }
        return render(request, 'review_list.html',context)
    def post(self, request, *args, **kwargs):
        formset = GearFormSet(request.POST or None, queryset=Gear.objects.all())
        print(formset)
        if formset.is_valid():
            instance = formset.save(commit=False)
            for inst in formset.deleted_objects:
                inst.delete()
            for form in instance:
                print(form)
                print('000000000000')
                form.save()
            formset = GearFormSet(queryset=Gear.objects.order_by('gear'))
            context = {
                'register_msg': '登録完了',
                'formset': formset
            }
            return render(request, 'register_gear.html',context)
        else:
            print(formset._errors)
            context = {
                'register_msg': formset._errors,
                'formset': formset
            }
            return render(request, 'register_gear.html',context)