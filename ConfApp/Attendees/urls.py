from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('Attendees/profile/<slug>', views.Profiles, name='Infos_page'),
    path('Attendees/search', views.searchpage, name='Attendees_search'),
    path('Attendees/profile', views.ProfilePage, name='profile_page'),

]
