from django.urls import path

from . import views


urlpatterns = [
    path('', views.activity_record, name='activity_record'),
    path('register_activity_record', views.register_activity_record, name='register_activity_record'),
    path('register_schedule', views.register_schedule, name='register_schedule'),
    path('activity_log', views.activity_log, name='activity_log'),
    path('activity_log/<str:today_jst_str>', views.activity_detail, name='activity_detail'),
    path('subject_log', views.subject_log, name='subject_log'),
]
