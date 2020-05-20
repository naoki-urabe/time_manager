from django.shortcuts import render, redirect
from django.views import View
from .models import ActiveRecord
from .models import Gear
from .models import Subject
from .models import KujiLog
from .models import Review
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import localtime
import datetime
from time import mktime
from .forms import ActiveRecordFormSet
from .forms import ActiveRecordForm
from .forms import SubjectFormSet
from .forms import GearFormSet
from .forms import ReviewFormSet
import re

# Create your views here.
class ActivityRecordView(View):
    def get(self, request, *args, **kwargs):
        
        latest_task_record = ActiveRecord.objects.filter(active_type='task').order_by('-today').first()
        task_exists = latest_task_record.is_active
        selected_task = latest_task_record if task_exists else None
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
        subject_logs = ActiveRecord.objects.filter(task=latest_task_record.task).order_by('-today')[:3] if task_name!='' else None
        subject_all = Subject.objects.all()
        gear_kind = Gear.objects.all().values_list('gear', flat=True).order_by('gear').distinct()
        for gear in gear_kind:
            print(gear)
        active_form = ActiveRecordForm(
            initial={
                'task':'active',
                'active_exists':active_exists,
                'active_id':active_id,
                'active_memo':active_memo,
                'active_type':'active'
                })
        task_form = ActiveRecordForm(
            initial={
                'task':task_name,
                'active_exists':task_exists,
                'active_id':task_id,
                'active_memo':task_memo,
                'active_type':'task'
                })
        review_formset = ReviewFormSet(request.POST or None, queryset=Review.objects.filter(today_date=localtime(timezone.now()).date()))
        todays_review = Review.objects.filter(Q(tomorrow=localtime(timezone.now()).date()) | 
                                              Q(one_week_later=localtime(timezone.now()).date()) |
                                              Q(two_week_later=localtime(timezone.now()).date()) | 
                                              Q(one_month_later=localtime(timezone.now()).date())).distinct()
        print(Review.objects.filter(tomorrow=localtime(timezone.now()).date()))
        print(Review.objects.filter(Q(tomorrow=localtime(timezone.now()))))
        print(todays_review)
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
            'subject_logs': subject_logs,
            'task_active_time': (latest_task_record.end_time if not latest_task_record.end_time is None else latest_task_record.begin_time).timestamp(),
            'subject_all': subject_all,
            'gear_kind': gear_kind,
            'review_formset': review_formset,
            'todays_review': todays_review
        }
        """
        context = {
            'has_already_today_active': has_already_today_active,
            'active_status' : active_status,
            'active_form': active_form,
            'task_form': task_form,
            'task_status': task_status,
            'today_activity': today_activities,
            'latest_kuji_log': latest_kuji_log,
            'gear': latest_kuji_log.gear_log,
            'subject_logs': subject_logs
        }
        """
        return render(request, 'activity_record.html', context)
    def post(self, request, *args, **kwargs):
        print(request.POST)
        if "kuji" in request.POST:

            latest_task_record = ActiveRecord.objects.filter(active_type='task').order_by('-today').first()
            task_exists = latest_task_record.is_active
            task_id = latest_task_record.id if task_exists else -1
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
            not_selected_subjects = Gear.objects.filter(gear=gear,latest_ver=0)
            query_count = not_selected_subjects.count()
            latest_ver = Gear.objects.filter(gear=gear).count() - query_count + 1
            if query_count == 0:
                latest_ver = 1
                update_subjects = []
                gear_subjects = Gear.objects.filter(gear=gear)
                for subject in gear_subjects:
                    subject.latest_ver = 0
                    update_subjects.append(subject)
                Gear.objects.bulk_update(update_subjects, fields=['latest_ver'])
                not_selected_subjects = Gear.objects.filter(gear=gear,latest_ver=0)
                query_count = not_selected_subjects.count()
            print('---------------not selected---------------')
            for s in not_selected_subjects:
                print(s.subject_id,s.latest_ver)
            print('-----------------------------------------')
            selected_subject = not_selected_subjects.order_by('?').first()
            selected_subject_id = selected_subject.subject_id
            selected_subject_name = Subject.objects.get(subject_id=selected_subject_id).subject
            print('--------------selected subject-------------')
            print(selected_subject_id,selected_subject_name)
            print('-------------------------------------------')
            selected_subject.latest_ver = latest_ver
            selected_subject.save()
            subject_logs = ActiveRecord.objects.filter(task=selected_subject_name).order_by('-today')[:3] if selected_subject_name!='' else None
            print(subject_logs)
            latest_kuji_log = KujiLog.objects.all().order_by('-today').first()
            if latest_kuji_log is None:
                KujiLog.objects.create(gear_log=gear,cycle_log=1,latest_ver=1,today=timezone.now(),subject=selected_subject_name,today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'))
            else:
                if latest_kuji_log.gear_log != gear:
                    KujiLog.objects.create(gear_log=gear,cycle_log=1,latest_ver=1,today=timezone.now(),subject=selected_subject_name,today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'))
                else:
                    if latest_ver==1:
                        KujiLog.objects.create(gear_log=gear,cycle_log=latest_kuji_log.cycle_log+1,latest_ver=1,today=timezone.now(),subject=selected_subject_name,today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'))
                    else:
                        KujiLog.objects.create(gear_log=gear,cycle_log=latest_kuji_log.cycle_log,latest_ver=latest_kuji_log.latest_ver+1,today=timezone.now(),subject=selected_subject_name,today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'))
            subject_all = Subject.objects.all()
            gear_kind = Gear.objects.all().values_list('gear', flat=True).order_by('gear').distinct()
            review_formset = ReviewFormSet(queryset=Review.objects.filter(today_date=localtime(timezone.now()).date()))
            context = {
                'task_name': selected_subject_name,
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
                'subject_logs': subject_logs,
                'task_active_time': (latest_task_record.end_time if not latest_task_record.end_time is None else latest_task_record.begin_time).timestamp(),
                'subject_all': subject_all,
                'gear_kind': gear_kind,
                'review_formset': review_formset
            }
            return render(request, 'activity_record.html', context)
        if "punch" in request.POST:
            active_form = ActiveRecordForm(request.POST)
            activity_id=request.POST['activity_id']
            active_type=request.POST['active_type']
            if activity_id=='-1':
                task_name=request.POST['task_name']
                active_record = ActiveRecord(task=task_name,begin_time=localtime(timezone.now()),today=timezone.now(),today_jst=localtime(timezone.now()),today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'),active_type=active_type,memo="")
                print(active_record.today_jst_str)
                active_record.save()
            else:
                memo = request.POST['memo']
                print(request.POST)
                active_record = ActiveRecord.objects.get(id=activity_id,active_type=active_type)
                active_record.end_time=localtime(timezone.now())
                active_record.period = timedelta_to_sec(active_record.end_time - active_record.begin_time)
                active_record.format_period = format_timedelta(active_record.period)
                print("format period "+active_record.format_period)
                active_record.is_active = False
                active_record.memo = memo
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
            subject_logs = ActiveRecord.objects.filter(task=latest_task_record.task).order_by('-today')[:3] if task_name!='' else None
            subject_all = Subject.objects.all()
            gear_kind = Gear.objects.all().values_list('gear', flat=True).order_by('gear').distinct()
            review_formset = ReviewFormSet(queryset=Review.objects.filter(today_date=localtime(timezone.now()).date()))
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
                'subject_logs': subject_logs,
                'task_active_time': (latest_task_record.end_time if not latest_task_record.end_time is None else latest_task_record.begin_time).timestamp(),
                'subject_all': subject_all,
                'gear_kind': gear_kind,
                'review_formset': review_formset
                
            }
            return render(request, 'activity_record.html', context)
        if "register_memo" in request.POST:
            print('right')
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
            subject_logs = ActiveRecord.objects.filter(task=latest_task_record.task).order_by('-today')[:3] if task_name!='' else None
            subject_all = Subject.objects.all()
            gear_kind = Gear.objects.all().values_list('gear', flat=True).order_by('gear').distinct()
            review_formset = ReviewFormSet(queryset=Review.objects.filter(today_date=localtime(timezone.now()).date()))
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
                'subject_logs': subject_logs,
                'task_active_time': (latest_task_record.end_time if not latest_task_record.end_time is None else latest_task_record.begin_time).timestamp(),
                'subject_all': subject_all,
                'gear_kind': gear_kind,
                'review_formset': review_formset
            }
            return render(request, 'activity_record.html', context)
        if "register_review" in request.POST:
            formset = ReviewFormSet(request.POST or None, queryset=Review.objects.none())
            if formset.is_valid():
                instances = formset.save(commit=False)
                print('##############################')
                print(instances)
                print('##############################')
                for inst in instances:
                    base_review_id = ("00000" + str(inst.version))[-5:]
                    inst.review_id = "P" + base_review_id if inst.is_online == 'online' else "N" + base_review_id
                    inst.today = localtime(timezone.now())
                    inst.today_date = localtime(timezone.now()).date()
                    inst.tomorrow = localtime(timezone.now()+datetime.timedelta(days=1)).date()
                    inst.one_week_later = localtime(timezone.now()+datetime.timedelta(days=7)).date()
                    inst.two_week_later = localtime(timezone.now()+datetime.timedelta(days=14)).date()
                    inst.one_month_later = localtime(timezone.now()+datetime.timedelta(days=28)).date()
                    print('---------------------------')
                    print(inst)
                    inst.save()
                    print('---------------------------')
                formset.save()
            
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
                subject_logs = ActiveRecord.objects.filter(task=latest_task_record.task).order_by('-today')[:3] if task_name!='' else None
                subject_all = Subject.objects.all()
                gear_kind = Gear.objects.all().values_list('gear', flat=True).order_by('gear').distinct()
                review_formset = ReviewFormSet(request.POST or None, queryset=Review.objects.filter(today_date=localtime(timezone.now()).date()))
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
                    'subject_logs': subject_logs,
                    'task_active_time': (latest_task_record.end_time if not latest_task_record.end_time is None else latest_task_record.begin_time).timestamp(),
                    'subject_all': subject_all,
                    'gear_kind': gear_kind,
                    'review_formset': review_formset
                }        
                return render(request, 'activity_record.html', context)
            else:
                print(formset.errors)
                return render(request, 'activity_record.html', context)

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
            'today_jst_str': today_jst_str
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

class RegisterSubjectView(View):
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

class RegisterGearView(View):
    def get(self, request, *args, **kwargs):
        formset = GearFormSet(queryset=Gear.objects.order_by('gear'))
        context = {
            'formset': formset
        }
        return render(request, 'register_gear.html',context)
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

class EditLogView(View):
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
                form.today_jst_str = localtime(timezone.now()).strftime('%Y%m%d')
                form.is_active = False
                form.period = timedelta_to_sec(form.end_time - form.begin_time)
                form.format_period = format_timedelta(form.period)
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
register_subject = RegisterSubjectView.as_view()
register_gear = RegisterGearView.as_view()
review_list = ReviewListView.as_view()
edit_log = EditLogView.as_view()