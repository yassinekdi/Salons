from django.shortcuts import render
import json
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required

@login_required
def room(request,room_slug):

    return render(request,'messaging/room.html', {
        'room_slug': mark_safe(json.dumps(room_slug)),
        'user_slug': mark_safe(json.dumps(request.user.slug))})
