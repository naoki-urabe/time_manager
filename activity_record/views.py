from django.shortcuts import render
from django.views import View
from .models import ActiveRecord
from .models import TaskRecord
from django.utils import timezone
import datetime

# Create your views here.
class ActivityRecordView(View):
    def get(self, request, *args, **kwargs):
        active_exists = self.get_active_exists()
        active_id = self.get_active_id(active_exists)
        task_exists = self.get_task_exists()
        task_id = self.get_task_id(task_exists)
        task_name = self.get_task_name(task_id)
        active_status = '活動中' if (active_exists) else '睡眠中'
        task_status = '進行中' if (task_exists) else '開始'
        context = {
            'active_exists': active_exists,
            'active_id': active_id,
            'active_status': active_status,
            'task_exists': task_exists,
            'task_id': task_id,
            'task_name': task_name,
            'task_status': task_status
        }
        return render(request, 'activity_record.html', context)
    def get_active_exists(self):
        active_exists = ActiveRecord.objects.filter(is_active=True).exists()
        return active_exists
    def get_active_id(self,active_exists):
        active_id = -1
        if active_exists:
            active_id =  ActiveRecord.objects.get(task='active',today=timezone.now().date(),is_active=True).id
        return active_id
    def get_task_exists(self):
        task_exists = TaskRecord.objects.filter(is_active=True).exists()
        return task_exists
    def get_task_id(self,task_exists):
        task_id = -1
        if task_exists:
            task_id = TaskRecord.objects.get(is_active=True).id
        return task_id
    def get_task_name(self,task_id):
        task_name = ""
        if task_id != -1:
            task_name = TaskRecord.objects.get(id = task_id).task
        return task_name
class RegisterActiveRecord(View):
    def post(self, request, *args, **kwargs):
        active_exists=request.POST['active_exists']
        if active_exists == 'True':
            active_record = ActiveRecord.objects.get(is_active=True)
            active_record.end_time=timezone.now()
            #task_record.period=task_record.end_time-task_record.begin_time
            active_record.is_active=False
            active_record.save()
        else:
            active_record = ActiveRecord(task='active',begin_time=timezone.now())
            active_record.save()
        context = {
            'active_status': "打刻完了",
            'now': timezone.now()
        }
        return render(request, 'register_active_record.html', context)
class RegisterTaskRecord(View):
    def post(self, request, *args, **kwargs):
        print("test")
        task_id=request.POST['task_id']
        if task_id=='-1':
            task_name=request.POST['task_name']
            task_record = TaskRecord(task=task_name,begin_time=timezone.now())
            task_record.save()
        else:
            task_record = TaskRecord.objects.get(id=task_id)
            task_record.end_time=timezone.now()
            #task_record.period = task_record.end_time - task_record.begin_time
            task_record.is_active = False
            task_record.save()
        context = {
            'active_status': "打刻完了",
            'now': timezone.now()
        }
        return render(request, 'register_task_record.html', context)
activity_record = ActivityRecordView.as_view()
register_active_record = RegisterActiveRecord.as_view()
register_task_record = RegisterTaskRecord.as_view()