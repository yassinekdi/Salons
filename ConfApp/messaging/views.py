from django.shortcuts import render
import json
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from .models import Discussion

@login_required
def room(request,room_slug):

    try:
        discussion_slug = Discussion.objects.get(slug=room_slug)
    except:
        discussion_slug = Discussion.objects.create(slug=room_slug)

    return render(request,'messaging/room.html', {
        'room_slug': mark_safe(json.dumps(room_slug)),
        'user_slug': mark_safe(json.dumps(request.user.slug)),
        'discussion_slug': mark_safe(json.dumps(discussion_slug.slug))
        })



