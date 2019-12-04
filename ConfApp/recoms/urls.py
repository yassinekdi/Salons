from django.contrib import admin
from django.urls import path, re_path
from . import views
from .views import RecomSessListView, RecomAtnListView

urlpatterns = [
    # path('', views.recoms, name='recoms'),
    path('recm_sessions/', RecomSessListView.as_view(), name='recoms_sess'),
    path('recm_attendees/', views.RecomAtnListView, name='recoms_atn'),
]

