from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('Attendees/profile/<slug>', views.Profiles, name='Infos_page'),
    path('<room_slug>/', views.room, name='room'),
]
