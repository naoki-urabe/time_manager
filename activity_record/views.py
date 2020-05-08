from django.shortcuts import render, redirect
from django.views import View
from .models import ActiveRecord
from .models import Subject
from .models import KujiLog
from django.utils import timezone
from django.utils.timezone import localtime
import datetime
from time import mktime
from .forms import ActiveRecordFormSet
import re

# Create your views here.
class ActivityRecordView(View):
    def get(self, request, *args, **kwargs):
        latest_task_record = ActiveRecord.objects.filter(active_type='task').order_by('-today').first()
        task_exists = latest_task_record.is_active
        task_id = latest_task_record.id if task_exists else -1
        task_name = latest_task_record.task if task_exists else ''
        task_memo = latest_task_record.memo if task_exists else ''
        task_status = '終了' if task_exists else '開始'
        latest_active_record = ActiveRecord.objects.filter(active_type='active').order_by('-today').first()
        active_exists = latest_active_record.is_active
        has_already_today_active =  localtime(timezone.now()).date()==latest_active_record.today_jst and not latest_active_record.is_active
        active_id = latest_active_record.id if active_exists else -1
        active_status = '活動中' if active_exists else '睡眠中'
        active_memo = latest_active_record.memo if active_exists else ''
        today_activities =  ActiveRecord.objects.filter(today_jst=latest_active_record.today_jst).order_by('-today')
        latest_kuji_log = KujiLog.objects.all().order_by('-today').first()
        subject_logs = ActiveRecord.objects.filter(task=latest_task_record.task).order_by('-today')[:3]
        context = {
            'active_exists': active_exists,
            'has_already_today_active': has_already_today_active,
            'active_id': active_id,
            'active_status' : active_status,
            'active_memo' : active_memo,
            'task_exists': task_exists,
            'task_id': task_id,
            'task_name': task_name,
            'task_memo' : task_memo,
            'task_status': task_status,
            'today_activity': today_activities,
            'latest_kuji_log': latest_kuji_log,
            'gear': latest_kuji_log.gear_log,
            'subject_logs': subject_logs
        }
        return render(request, 'activity_record.html', context)
    def post(self, request, *args, **kwargs):
        if "kuji" in request.POST:

            latest_task_record = ActiveRecord.objects.filter(active_type='task').order_by('-today').first()
            task_exists = latest_task_record.is_active
            task_id = latest_task_record.id if task_exists else -1
            task_name = latest_task_record.task if task_exists else ''
            task_memo = latest_task_record.memo if task_exists else ''
            task_status = '終了' if task_exists else '開始'
            latest_active_record = ActiveRecord.objects.filter(active_type='active').order_by('-today').first()
            active_exists = latest_active_record.is_active
            has_already_today_active =  localtime(timezone.now()).date()==latest_active_record.today_jst and not latest_active_record.is_active
            active_id = latest_active_record.id if active_exists else -1
            active_status = '活動中' if active_exists else '睡眠中'
            active_memo = latest_active_record.memo if active_exists else ''
            today_activities =  ActiveRecord.objects.filter(today_jst=latest_active_record.today_jst).order_by('-today')
            latest_kuji_log = KujiLog.objects.all().order_by('-today').first()

            gear = int(request.POST['gear'])
            subjects = Subject.objects.filter(gear=gear,latest=0)
            n = Subject.objects.filter(gear=gear).count()
            query_count = subjects.count()
            if query_count == 0:
                update_subjects = []
                gear_subjects = Subject.objects.filter(gear=gear)
                for subject in gear_subjects:
                    subject.latest = 0
                    update_subjects.append(subject)
                Subject.objects.bulk_update(update_subjects, fields=['latest'])
                subjects = Subject.objects.filter(gear=gear,latest=0)
                query_count = subjects.count()
            selected_subject = subjects.order_by('?').first()
            selected_subject.latest = n-query_count+1
            selected_subject.save()
            subject_logs = ActiveRecord.objects.filter(task=latest_task_record.task).order_by('-today')[:3]
            print(subject_logs)
            latest_kuji_log = KujiLog.objects.all().order_by('-today').first()
            if latest_kuji_log is None:
                KujiLog.objects.create(gear_log=gear,cycle_log=1,latest_ver=1,today=timezone.now(),subject=selected_subject.subject,today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'))
            else:
                if latest_kuji_log.gear_log != gear:
                    KujiLog.objects.create(gear_log=gear,cycle_log=1,latest_ver=1,today=timezone.now(),subject=selected_subject.subject,today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'))
                else:
                    if n-query_count==0:
                        KujiLog.objects.create(gear_log=gear,cycle_log=latest_kuji_log.cycle_log+1,latest_ver=1,today=timezone.now(),subject=selected_subject.subject,today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'))
                    else:
                        KujiLog.objects.create(gear_log=gear,cycle_log=latest_kuji_log.cycle_log,latest_ver=latest_kuji_log.latest_ver+1,today=timezone.now(),subject=selected_subject.subject,today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'))
            context = {
                'task_name': selected_subject.subject,
                'gear': gear,
                'active_status': request.POST['active_status'],
                'task_status': request.POST['task_status'],
                'active_exists': active_exists,
                'has_already_today_active': has_already_today_active,
                'active_id': active_id,
                'active_memo' : active_memo,
                'task_exists': task_exists,
                'task_id': task_id,
                'task_memo' : task_memo,
                'today_activity': today_activities,
                'latest_kuji_log': latest_kuji_log,
                'subject_logs': subject_logs
            }
            return render(request, 'activity_record.html', context)
        if "punch" in request.POST:
            activity_id=request.POST['activity_id']
            active_type=request.POST['active_type']
            if activity_id=='-1':
                task_name=request.POST['task_name']
                active_record = ActiveRecord(task=task_name,begin_time=localtime(timezone.now()),today=timezone.now(),today_jst=localtime(timezone.now()),today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'),active_type=active_type,memo="")
                print(active_record.today_jst_str)
                active_record.save()
            else:
                #memo = request.POST['memo']
                print(request.POST)
                active_record = ActiveRecord.objects.get(id=activity_id,active_type=active_type)
                active_record.end_time=localtime(timezone.now())
                active_record.period = timedelta_to_sec(active_record.end_time - active_record.begin_time)
                active_record.format_period = format_timedelta(active_record.period)
                print("format period "+active_record.format_period)
                active_record.is_active = False
                #active_record.memo = memo
                active_record.save()
            latest_task_record = ActiveRecord.objects.filter(active_type='task').order_by('-today').first()
            task_exists = latest_task_record.is_active
            task_id = latest_task_record.id if task_exists else -1
            task_name = latest_task_record.task if task_exists else ''
            task_memo = latest_task_record.memo if task_exists else ''
            task_status = '終了' if task_exists else '開始'
            latest_active_record = ActiveRecord.objects.filter(active_type='active').order_by('-today').first()
            active_exists = latest_active_record.is_active
            has_already_today_active =  localtime(timezone.now()).date()==latest_active_record.today_jst and not latest_active_record.is_active
            active_id = latest_active_record.id if active_exists else -1
            active_status = '活動中' if active_exists else '睡眠中'
            active_memo = latest_active_record.memo if active_exists else ''
            today_activities =  ActiveRecord.objects.filter(today_jst=latest_active_record.today_jst).order_by('-today')
            latest_kuji_log = KujiLog.objects.all().order_by('-today').first()
            subject_logs = ActiveRecord.objects.filter(task=latest_task_record.task).order_by('-today')[:3]
            context = {
                'active_exists': active_exists,
                'has_already_today_active': has_already_today_active,
                'active_id': active_id,
                'active_status': active_status,
                'active_memo' : active_memo,
                'task_exists': task_exists,
                'task_id': task_id,
                'task_name': task_name,
                'task_memo' : task_memo,
                'task_status': task_status,
                'today_activity': today_activities,
                'latest_kuji_log': latest_kuji_log,
                'gear': latest_kuji_log.gear_log,
                'subject_logs': subject_logs 
            }
            return render(request, 'activity_record.html', context)
        if "register_memo" in request.POST:
            activity_id=request.POST['activity_id']
            active_record = ActiveRecord.objects.filter(id=activity_id).first()
            active_record.memo = request.POST['memo']
            active_record.save()
            latest_task_record = ActiveRecord.objects.filter(active_type='task').order_by('-today').first()
            task_exists = latest_task_record.is_active
            task_id = latest_task_record.id if task_exists else -1
            task_name = latest_task_record.task if task_exists else ''
            task_memo = latest_task_record.memo if task_exists else ''
            task_status = '終了' if task_exists else '開始'
            latest_active_record = ActiveRecord.objects.filter(active_type='active').order_by('-today').first()
            active_exists = latest_active_record.is_active
            has_already_today_active =  localtime(timezone.now()).date()==latest_active_record.today_jst and not latest_active_record.is_active
            active_id = latest_active_record.id if active_exists else -1
            active_status = '活動中' if active_exists else '睡眠中'
            active_memo = latest_active_record.memo if active_exists else ''
            today_activities =  ActiveRecord.objects.filter(today_jst=latest_active_record.today_jst).order_by('-today')
            latest_kuji_log = KujiLog.objects.all().order_by('-today').first()

            context = {
                'active_exists': active_exists,
                'has_already_today_active': has_already_today_active,
                'active_id': active_id,
                'active_status': active_status,
                'active_memo' : active_memo,
                'task_exists': task_exists,
                'task_id': task_id,
                'task_name': task_name,
                'task_memo' : task_memo,
                'task_status': task_status,
                'today_activity': today_activities,
                'latest_kuji_log': latest_kuji_log,
                'gear': latest_kuji_log.gear_log,
                'subject_logs': None
            }
            return render(request, 'activity_record.html', context)
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
                    if not re.search('(予)',schedule.task):
                        schedule.task = schedule.task + '(予)'
                    if not schedule.today:
                        schedule.today_jst = schedule.today.date
                    if not schedule.today_jst:
                        schedule.today_jst_str = schedule.today.date().strftime('%Y%m%d')
                    schedule.is_active = False
                    form.save()
                else:
                    if schedule.end_time != None:
                        schedule.is_active = False
                        schedule.period = timedelta_to_sec(schedule.end_time - schedule.begin_time)
                        schedule.format_period = format_timedelta(schedule.period)
                    elif schedule.begin_time != None:
                        schedule.is_active = True
                    schedule.save()
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
        active_histories = ActiveRecord.objects.filter(today_jst_str=today_jst_str).order_by('-today')
        print(active_histories)
        context = {
            'today_activity': active_histories,
        }
        return render(request, 'log_detail.html', context)
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

def to_jst(time):
    print((time + datetime.timedelta(hours=9)).date())
    return (time + datetime.timedelta(hours=9)).date()
def format_timedelta(sec):
    hours=sec//3600
    minutes=(sec%3600)//60
    seconds=(sec%3600)%60
    return "{0:02d}:{1:02d}:{2:02d}".format(hours,minutes,seconds)
def timedelta_to_sec(timedelta):
    sec = timedelta.days*86400 + timedelta.seconds
    return sec
def check_activity_exists(active_type,today_jst):
    activity_exists = ActiveRecord.objects.filter(is_active=True,active_type=active_type,today_jst=today_jst).exists()
    return activity_exists    
def check_todays_active_exists(today_jst):
    todays_active_exists = ActiveRecord.objects.filter(active_type="active",today_jst=today_jst).exists()
    return todays_active_exists 
def get_activity_histories(today_jst):
    activity_histories = ActiveRecord.objects.filter(today_jst=today_jst).order_by('-today')
    return activity_histories
def get_activity_id(today_jst,active_exists,active_type):
    active_id = -1
    if active_exists:
        active_id =  ActiveRecord.objects.get(today_jst=today_jst,is_active=True,active_type=active_type).id
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
    all_active_logs = ActiveRecord.objects.filter(active_type='active').order_by('-today')
    print(all_active_logs)
    return all_active_logs

activity_record = ActivityRecordView.as_view()
register_schedule = RegisterScheduleView.as_view()
activity_log = ActivityLogView.as_view()
activity_detail = ActivityDetailView.as_view()
subject_log = SubjectLogView.as_view()