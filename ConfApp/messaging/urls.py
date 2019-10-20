from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('Attendees/profile/<slug>', views.Profiles, name='Infos_page'),
    path('<room_slug>/', views.newroom, name='room'),
    path('new/newroom/',views.room,name='new_room')
]
