from django.shortcuts import render
from recoms.models import Theme, Session
import datetime
import random

def give_durations(session,dur):
    session.Start_time = datetime.datetime.strptime(dur[0],'%H:%M')
    session.Final_time = datetime.datetime.strptime(dur[1],'%H:%M')
    return session

def program(request):

    # Times to be given in calendar models after
    Time = ['09:00','09:15','09:30','09:45','10:00','10:15','10:30','10:45','11:00']
    Durations = [(a,b) for a,b in zip(Time[:-1],Time[1:])]
    themes = Theme.objects.all()

    # ------------- We define start/final times for sessions -----------------------

    # Keynotes starts at 9:00, finishes at 10:00 - we have 3 sessions in kynote
    th_Keynote = Theme.objects.get(title='Keynote Lectures')
    th_Keynote_Duration = Durations[:3]
    th_Keynote_sess = th_Keynote.sessions.all()
    for sess,dur in zip(th_Keynote_sess, th_Keynote_Duration):
        sess=give_durations(sess,dur)
        sess.save()
    # We give random times for 5 (themes) x 6 sessions/day
    # Other themes start at 9:30
    sessions_Duration = Durations[3:]
    other_themes = Theme.objects.exclude(title="Keynote Lectures")
    sessions= {}
    for theme in other_themes:
        sessions[theme.title] = theme.sessions.all()[:6]
        for sess, dur in zip(sessions[theme.title],sessions_Duration):
            sess = give_durations(sess,dur)
            sess.save()


    # ------------- We check in each duration





    return render(request, 'Calendar/calendar.html')