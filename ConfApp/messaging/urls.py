from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<disc_slug>/', views.room, name='room'),
]
