from django.urls import path

from . import views


urlpatterns = [
    path('', views.activity_record, name='activity_record'),
    path('register_active_record', views.register_active_record, name='register_active_record'),
    path('register_task_record', views.register_task_record, name='register_task_record'),
]
