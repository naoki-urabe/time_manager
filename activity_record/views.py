from django.shortcuts import render, redirect
from django.views import View
from .models import ActiveRecord
from django.utils import timezone
from django.utils.timezone import localtime
import datetime
from time import mktime
from .forms import ActiveRecordFormSet
import re

# Create your views here.
class ActivityRecordView(View):
    def get(self, request, *args, **kwargs):
        active_exists = check_activity_exists("active")
        todays_active_exists = check_todays_active_exists()
        active_id = get_activity_id(active_exists,"active")
        active_histories = get_activity_histories()
        active_memo = get_memo(active_id,"active")
        task_exists = check_activity_exists("task")
        task_id = get_activity_id(task_exists,"task")
        task_name = get_task_name(task_id)
        task_memo = get_memo(task_id,"task")
        active_status = '活動中' if (active_exists) else '睡眠中'
        task_status = '終了' if (task_exists) else '開始'
        context = {
            'active_exists': active_exists,
            'todays_active_exists': todays_active_exists,
            'active_id': active_id,
            'active_status': active_status,
            'active_memo' : active_memo,
            'task_exists': task_exists,
            'task_id': task_id,
            'task_name': task_name,
            'task_memo' : task_memo,
            'task_status': task_status,
            'today_activity': active_histories,
        }
        return render(request, 'activity_record.html', context)
class RegisterActivityRecord(View):
    def post(self, request, *args, **kwargs):
        if "punch" in request.POST:
            activity_id=request.POST['activity_id']
            active_type=request.POST['active_type']
            if activity_id=='-1':
                task_name=request.POST['task_name']
                active_record = ActiveRecord(task=task_name,begin_time=localtime(timezone.now()),today=timezone.now(),today_jst=to_jst(timezone.now()),today_jst_str=to_jst(timezone.now()).strftime('%Y%m%d'),active_type=active_type,memo="")
                print(active_record.today_jst_str)
                active_record.save()
            else:
                #memo = request.POST['memo']
                active_record = ActiveRecord.objects.get(id=activity_id,active_type=active_type)
                active_record.end_time=localtime(timezone.now())
                active_record.period = timedelta_to_sec(active_record.end_time - active_record.begin_time)
                active_record.format_period = format_timedelta(active_record.period)
                print("format period "+active_record.format_period)
                active_record.is_active = False
                #active_record.memo = memo
                active_record.save()
            context = {
                'active_status': "打刻完了",
                'now': timezone.now()
            }
            return render(request, 'register_active_record.html', context)
        if "register_memo" in request.POST:
            activity_id=request.POST['activity_id']
            active_record = ActiveRecord.objects.filter(id=activity_id).first()
            active_record.memo = request.POST['memo']
            active_record.save()
            context = {
                'active_status': "メモ登録完了",
                'now': timezone.now()
            }
            return render(request, 'register_active_record.html', context)

class RegisterScheduleView(View):
    def get(self, request, *args, **kwargs):
        formset = ActiveRecordFormSet()
        context = {
        'formset':formset
        }
        return render(request,'register_schedule.html', context)
        
    def post(self, request, *args, **kwargs):
        formset = ActiveRecordFormSet(request.POST or None, queryset=ActiveRecord.objects.filter(begin_time__lte=localtime(timezone.now())))
        if formset.is_valid():
            
            for form in formset:
                schedule = form.save(commit=False)
                if schedule.task == None:
                    continue
                if schedule.active_type == "schedule":
                    schedule = form.save(commit=False)
                    print('im here')
                    if not re.search('(予)',schedule.task):
                        schedule.task = schedule.task + '(予)'
                    if not schedule.today:
                        schedule.today_jst = schedule.today.date
                    if not schedule.today_jst:
                        schedule.today_jst_str = schedule.today.date().strftime('%Y%m%d')
                    schedule.is_active = False
                    form.save()
                else:
                    form.save()
            #for obj in formset.deleted_objects:
                #obj.delete()
            formset = ActiveRecordFormSet()
            context = {
                'register_success_msg':"登録完了",
                'formset':formset
            }
            return render(request, 'register_schedule.html',context)
        else:
            print(formset.errors)
            context = {
                'formset':formset
            }
            return render(request, 'register_schedule.html',context)
class ActivityLogView(View):
    def get(self, request, *args, **kwargs):
        all_active_logs = get_all_active_logs()
        context = {
                'all_active_logs':all_active_logs
            }
        return render(request, 'show_logs.html',context)
class ActivityDetailView(View):
    def get(self, request,today_jst_str, *args, **kwargs):
        active_histories = ActiveRecord.objects.filter(today_jst_str=today_jst_str)
        print(active_histories)
        context = {
            'today_activity': active_histories,
        }
        return render(request, 'log_detail.html', context)
def to_jst(time):
    print((time + datetime.timedelta(hours=9)).date())
    return (time + datetime.timedelta(hours=9)).date()
def to_utc(time):
    print(time - datetime.timedelta(hours=9))
    return time - datetime.timedelta(hours=9)
def format_timedelta(sec):
    hours=sec//3600
    minutes=(sec%3600)//60
    seconds=(sec%3600)%60
    return "{0:02d}:{1:02d}:{2:02d}".format(hours,minutes,seconds)
def timedelta_to_sec(timedelta):
    sec = timedelta.days*86400 + timedelta.seconds
    return sec
def check_activity_exists(active_type):
    activity_exists = ActiveRecord.objects.filter(is_active=True,active_type=active_type,today_jst=localtime(timezone.now())).exists()
    return activity_exists    
def check_todays_active_exists():
    todays_active_exists = ActiveRecord.objects.filter(active_type="active",today_jst=localtime(timezone.now())).exists()
    return todays_active_exists       
def get_activity_histories():
    activity_histories = ActiveRecord.objects.filter(today_jst=localtime(timezone.now()))
    return activity_histories
def get_activity_id(active_exists,active_type):
    active_id = -1
    if active_exists:
        active_id =  ActiveRecord.objects.get(today_jst=to_jst(timezone.now()),is_active=True,active_type=active_type).id
    return active_id
def get_task_name(task_id):
    task_name = ""
    if task_id != -1:
        task_name = ActiveRecord.objects.get(id = task_id,active_type='task').task
    return task_name
def get_memo(task_id,active_type):
    task_memo = ""
    if task_id != -1:
        task_memo = ActiveRecord.objects.get(id = task_id,active_type=active_type).memo
    return task_memo
def get_all_active_logs():
    all_active_logs = ActiveRecord.objects.filter(active_type='active')
    print(all_active_logs)
    return all_active_logs
activity_record = ActivityRecordView.as_view()
register_activity_record = RegisterActivityRecord.as_view()
register_schedule = RegisterScheduleView.as_view()
activity_log = ActivityLogView.as_view()
activity_detail = ActivityDetailView.as_view()