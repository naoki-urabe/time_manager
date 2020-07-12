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
from activity_record.modules import load_logs
from django.db.models import Sum

class ActivityRecordView(View):
    def get(self, request, *args, **kwargs):
        task_logs = load_logs.load_logs("task")
        latest_task_log = task_logs.first()
        task_log_info = load_logs.load_log_info(latest_task_log)
        active_logs = load_logs.load_logs("active")
        latest_active_log = active_logs.first()
        """
        active_record_list = ActiveRecord.objects.filter(active_type='active').order_by('-today')
        print(active_record_list)
        yesterday_active_record = None
        if len(active_record_list) > 2:
            yesterday_active_record = ActiveRecord.objects.filter(active_type='active').order_by('-today')[1] if ActiveRecord.objects.filter(active_type='active')!=None else None 
        """
        active_log_info = load_logs.load_log_info(latest_active_log)
        
        has_already_today_active =  localtime(timezone.now()).date()==latest_active_record.today_jst and not latest_active_record.is_active
        
        today_activities =  ActiveRecord.objects.filter(today_jst_str=latest_active_record.today_jst_str).order_by('-today')
        latest_kuji_log = KujiLog.objects.all().order_by('-today').first()
        subject_logs = ActiveRecord.objects.filter(task=latest_task_record.task).order_by('-today')[:3] if task_name!='' else None
        subject_all = Subject.objects.all()
        gear_kind = Gear.objects.all().values_list('gear', flat=True).order_by('gear').distinct()
        today_study_time_sum_dic = ActiveRecord.objects.filter(active_type="study",today_jst_str=latest_active_record.today_jst_str).aggregate(Sum('period'))
        yesterday_study_time_sum_dic = ActiveRecord.objects.filter(active_type="study",today_jst_str=yesterday_active_record.today_jst_str).aggregate(Sum('period'))
        today_study_time_sum = int(today_study_time_sum_dic['period__sum']) if today_study_time_sum_dic['period__sum'] != None else 0
        yesterday_study_time_sum = int(yesterday_study_time_sum_dic['period__sum']) if yesterday_study_time_sum_dic['period__sum'] != None else 0
        compare_percentage = module.compare_study_amount(today_study_time_sum, yesterday_study_time_sum) if yesterday_study_time_sum != 0 else 0
        compare_percentage_msg = "{:.2f}".format(abs(compare_percentage))+"%減" if compare_percentage < 0 else "{:.2f}".format(compare_percentage)+"%増"
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
            'todays_review': todays_review,
            'today_study_time_sum': module.format_timedelta(today_study_time_sum),
            'yesterday_study_time_sum': module.format_timedelta(yesterday_study_time_sum),
            'compare_percentage_msg': compare_percentage_msg
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
        latest_active_record = ActiveRecord.objects.filter(active_type='active').order_by('-today').first()
        yesterday_active_record = ActiveRecord.objects.filter(active_type='active').order_by('-today')[1]
        today_study_time_sum_dic = ActiveRecord.objects.filter(active_type="study",today_jst_str=latest_active_record.today_jst_str).aggregate(Sum('period'))
        yesterday_study_time_sum_dic = ActiveRecord.objects.filter(active_type="study",today_jst_str=yesterday_active_record.today_jst_str).aggregate(Sum('period'))
        today_study_time_sum = int(today_study_time_sum_dic['period__sum']) if today_study_time_sum_dic['period__sum'] != None else 0
        yesterday_study_time_sum = int(yesterday_study_time_sum_dic['period__sum']) if yesterday_study_time_sum_dic['period__sum'] != None else 0
        compare_percentage = module.compare_study_amount(today_study_time_sum, yesterday_study_time_sum) if yesterday_study_time_sum != 0 else 0
        compare_percentage_msg =  "{:.2f}".format(abs(compare_percentage))+"%減" if compare_percentage < 0 else  "{:.2f}".format(compare_percentage)+"%増"
        if "kuji" in request.POST:
            latest_task_record = ActiveRecord.objects.exclude(active_type='task').order_by('-today').first()
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
            today_activities =  ActiveRecord.objects.filter(today_jst_str=latest_active_record.today_jst_str).order_by('-today')
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
                'review_formset': review_formset,
                'today_study_time_sum': module.format_timedelta(today_study_time_sum),
                'yesterday_study_time_sum': module.format_timedelta(yesterday_study_time_sum),
                'compare_percentage': compare_percentage,
                'compare_percentage_msg': compare_percentage_msg
            }
            return render(request, 'activity_record.html', context)
        if "punch" in request.POST:
            active_form = ActiveRecordForm(request.POST)
            activity_id=request.POST['activity_id']
            if activity_id=='-1':
                task_name=request.POST['task_name']
                active_type = ""
                if task_name != "active":
                    active_type = Subject.objects.get(subject=task_name).subject_type
                else:
                    active_type = "active"
                active_record = ActiveRecord(task=task_name,begin_time=localtime(timezone.now()),today=timezone.now(),today_jst=localtime(timezone.now()),today_jst_str=localtime(timezone.now()).strftime('%Y%m%d'),active_type=active_type,memo="")
                print(active_record.today_jst_str)
                active_record.save()
            else:
                memo = request.POST['memo']
                print(request.POST)
                active_record = ActiveRecord.objects.get(id=activity_id)
                active_record.end_time=localtime(timezone.now())
                active_record.period = module.timedelta_to_sec(active_record.end_time - active_record.begin_time)
                active_record.format_period = module.format_timedelta(active_record.period)
                print("format period "+active_record.format_period)
                active_record.is_active = False
                active_record.memo = memo
                if request.POST["task_name"] == "active":
                    today_study_time_sum_dic = ActiveRecord.objects.filter(active_type='study',today_jst_str=latest_active_record.today_jst_str).aggregate(Sum('period'))
                    print(today_study_time_sum_dic)
                    today_study_time_sum = int(today_study_time_sum_dic['period__sum']) if today_study_time_sum_dic['period__sum'] != None else 0
                    active_record.study_amount = today_study_time_sum
                    active_record.format_study_amount = module.format_timedelta(today_study_time_sum)
                active_record.save()
            latest_task_record = ActiveRecord.objects.exclude(active_type='active').order_by('-today').first()
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
            today_activities =  ActiveRecord.objects.filter(today_jst_str=latest_active_record.today_jst_str).order_by('-today')
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
                'review_formset': review_formset,
                'today_study_time_sum': module.format_timedelta(today_study_time_sum),
                'yesterday_study_time_sum': module.format_timedelta(yesterday_study_time_sum),
                'compare_percentage': compare_percentage,
                'compare_percentage_msg': compare_percentage_msg
            }
            return render(request, 'activity_record.html', context)
        if "register_memo" in request.POST:
            activity_id=request.POST['activity_id']
            active_record = ActiveRecord.objects.filter(id=activity_id).first()
            active_record.memo = request.POST['memo']
            active_record.save()
            latest_task_record = ActiveRecord.objects.exclude(active_type='active').order_by('-today').first()
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
            today_activities =  ActiveRecord.objects.filter(today_jst_str=latest_active_record.today_jst_str).order_by('-today')
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
                'review_formset': review_formset,
                'today_study_time_sum': module.format_timedelta(today_study_time_sum),
                'yesterday_study_time_sum': module.format_timedelta(yesterday_study_time_sum),
                'compare_percentage': compare_percentage,
                'compare_percentage_msg': compare_percentage_msg
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
            
                latest_task_record = ActiveRecord.objects.exclude(active_type='task').order_by('-today').first()
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
                today_activities =  ActiveRecord.objects.filter(today_jst_str=latest_active_record.today_jst_str).order_by('-today')
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
                    'review_formset': review_formset,
                    'today_study_time_sum': module.format_timedelta(today_study_time_sum),
                    'yesterday_study_time_sum': module.format_timedelta(yesterday_study_time_sum),
                    'compare_percentage': compare_percentage,
                    'compare_percentage_msg': compare_percentage_msg
                }        
                return render(request, 'activity_record.html', context)
            else:
                print(formset.errors)
                return render(request, 'activity_record.html', context)