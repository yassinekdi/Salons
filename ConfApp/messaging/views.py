from django.shortcuts import render
import json
from django.utils.safestring import mark_safe

def room(request,room_slug):
    return render(request, 'messaging/room.html',{'room_slug': mark_safe(json.dumps(room_slug))})
