from django.shortcuts import render, redirect
from django.views import View
from .models import ActiveRecord
from django.utils import timezone
from django.utils.timezone import localtime
import datetime
from time import mktime
from .forms import ActiveRecordFormSet

# Create your views here.
class ActivityRecordView(View):
    def get(self, request, *args, **kwargs):
        active_exists = self.check_activity_exists("active")
        active_id = self.get_activity_id(active_exists,"active")
        active_histories = self.get_activity_histories()
        task_exists = self.check_activity_exists("task")
        task_id = self.get_activity_id(task_exists,"task")
        task_name = self.get_task_name(task_id)
        active_status = '活動中' if (active_exists) else '睡眠中'
        task_status = '終了' if (task_exists) else '開始'
        context = {
            'active_exists': active_exists,
            'active_id': active_id,
            'active_status': active_status,
            'task_exists': task_exists,
            'task_id': task_id,
            'task_name': task_name,
            'task_status': task_status,
            'today_activity': active_histories,
        }
        return render(request, 'activity_record.html', context)
    def check_activity_exists(self,active_type):
        activity_exists = ActiveRecord.objects.filter(is_active=True,active_type=active_type,today_jst=localtime(timezone.now())).exists()
        return activity_exists    
    def get_activity_histories(self):
        activity_histories = ActiveRecord.objects.filter(today_jst=localtime(timezone.now()))
        return activity_histories
    def get_activity_id(self,active_exists,active_type):
        active_id = -1
        if active_exists:
            active_id =  ActiveRecord.objects.get(today_jst=to_jst(timezone.now()),is_active=True,active_type=active_type).id
        return active_id
    def get_task_name(self,task_id):
        task_name = ""
        if task_id != -1:
            task_name = ActiveRecord.objects.get(id = task_id,active_type='task').task
        return task_name
class RegisterActivityRecord(View):
    def post(self, request, *args, **kwargs):
        activity_id=request.POST['activity_id']
        active_type=request.POST['active_type']
        if activity_id=='-1':
            task_name=request.POST['task_name']
            active_record = ActiveRecord(task=task_name,begin_time=localtime(timezone.now()),today=timezone.now(),today_jst=to_jst(timezone.now()),active_type=active_type)
            active_record.save()
        else:
            active_record = ActiveRecord.objects.get(id=activity_id,active_type=active_type)
            active_record.end_time=localtime(timezone.now())
            active_record.period = timedelta_to_sec(active_record.end_time - active_record.begin_time)
            active_record.is_active = False
            active_record.today_jst = to_jst(timezone.now())
            active_record.save()
        context = {
            'active_status': "打刻完了",
            'now': timezone.now()
        }
        return render(request, 'register_active_record.html', context)
class RegisterScheduleView(View):
    def get(self, request, *args, **kwargs):
        print('get')
        formset = ActiveRecordFormSet()
        context = {
        'formset':formset
        }
        return render(request,'register_schedule.html', context)
        
    def post(self, request, *args, **kwargs):
        print(request.POST)
        formset = ActiveRecordFormSet(request.POST or None)
        if formset.is_valid():
            formset.save() 
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
def to_jst(time):
    print((time + datetime.timedelta(hours=9)).date())
    return (time + datetime.timedelta(hours=9)).date()
def timedelta_to_sec(timedelta):
    sec = timedelta.days*86400 + timedelta.seconds
    return sec
activity_record = ActivityRecordView.as_view()
register_activity_record = RegisterActivityRecord.as_view()
register_schedule = RegisterScheduleView.as_view()