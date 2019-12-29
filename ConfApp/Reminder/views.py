from django.shortcuts import render
from recoms.models import Session

def reminder_sessions(request):

    return render(request, 'Reminder/reminder_sessions.html')
