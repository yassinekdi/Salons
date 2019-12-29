from django.contrib import admin
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.reminder_sessions, name='reminder_sessions'),
]

