from django.shortcuts import render
from django.views import View

# Create your views here.
class ActivityRecordView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'msg': "hello"
        }
        return render(request, 'activity_record.html', context)

class Test(View):
    def post(self, request, *args, **kwargs):
        now = (request.POST['status'])
        context = {
            'msg': "打刻完了"
        }
        return render(request, 'test.html', context)
activity_record = ActivityRecordView.as_view()
test = Test.as_view()