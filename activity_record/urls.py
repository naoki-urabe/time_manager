from django.urls import path

from . import views


urlpatterns = [
    path('', views.activity_record, name='activity_record'),
]
