from django.shortcuts import render
from django.views import View

# Create your views here.
class ActivityRecordView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'msg': "hello"
        }
        return render(request, 'activity_record.html', context)
activity_record = ActivityRecordView.as_view()