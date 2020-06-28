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

def format_timedelta(sec):
    hours=sec//3600
    minutes=(sec%3600)//60
    seconds=(sec%3600)%60
    return "{0:02d}:{1:02d}:{2:02d}".format(hours,minutes,seconds)
def timedelta_to_sec(timedelta):
    sec = timedelta.days*86400 + timedelta.seconds
    return sec   

def get_all_active_logs():
    all_active_logs = ActiveRecord.objects.filter(active_type='active').order_by('-today')
    print(all_active_logs)
    return all_active_logs

def compare_study_amount(today_study_time_sum, yesterday_study_time_sum):
    print(today_study_time_sum, yesterday_study_time_sum)
    return (today_study_time_sum/yesterday_study_time_sum)*100 - 100
