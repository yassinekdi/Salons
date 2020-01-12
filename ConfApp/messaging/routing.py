# chat/routing.py
from django.urls import path,re_path
from django.conf.urls import url
from .consumers import ChatConsumer
from Attendees.consumers import Notifs

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_slug>[^/]+)', ChatConsumer),
    path('ws/chat/<disc_slug>/', ChatConsumer),
    path('home/', Notifs)
]
