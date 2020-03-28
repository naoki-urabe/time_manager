from django.urls import path

from . import views


urlpatterns = [
    path('', views.activity_record, name='activity_record'),
    path('register_activity_record', views.register_activity_record, name='register_activity_record'),
]
