from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry, name="entry"),
    path('new_conf/', views.new_conf, name="new_conf"),
]
