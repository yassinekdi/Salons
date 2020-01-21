from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.program, name='calendar'),
    path('<sess_id>/', views.add_sess_reminder, name='add_reminder'),
    path('<sess_id>/r', views.remove_sess_reminder, name='remove_reminder'),
    path('editing_calendar', views.edit_program, name='editing_program'),
]
