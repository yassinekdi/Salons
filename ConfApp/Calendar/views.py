from django.shortcuts import render, redirect
from recoms.models import Theme, Session
from django.http import HttpResponseRedirect
import datetime
import random

def give_durations(session,dur):
    # session.Start_time = datetime.datetime.strptime(dur[0],'%H:%M')
    # session.Final_time = datetime.datetime.strptime(dur[1],'%H:%M')


    session.Start_timeC = dur[0]
    session.Final_timeC = dur[1]
    return session

def organize_sessions(sessions,time):
    new_sessions=[]
    empty_session = Session.objects.get(Authors="noone")
    i = 0
    for sess in sessions:

            while sess.Start_timeC != time[i]:
                new_sessions.append(empty_session)
                i += 1
                if time[i]==time[-1]:
                    break
            new_sessions.append(sess)
            i+=1


    if len(new_sessions)<len(time):
        difference = len(time)-len(new_sessions)
        new_sessions = new_sessions + [empty_session]*difference
    return new_sessions


def program(request):

    # Times to be given in calendar models after
    Time = ['09:00','09:15','09:30','09:45','10:00','10:15','10:30','10:45','11:00','11:15']
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
    th_Keynote_sess2 = organize_sessions(th_Keynote_sess,Time[:-1])


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
        sessions[theme.title] = organize_sessions(sessions[theme.title], Time[:-1])

    sessions2 = [th_Keynote_sess2]+ [sessions[thm] for thm in sessions]

    context = {'times': Time,
               'themes_sessions': zip(themes, sessions2),
               'Duration': Durations}




    return render(request, 'Calendar/calendar.html', context)


def add_sess_reminder(request, sess_id):

    session = Session.objects.get(id=sess_id)
    session.Reminded_users.add(request.user)
    session.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_sess_reminder(request, sess_id):

    session = Session.objects.get(id=sess_id)
    session.Reminded_users.remove(request.user)
    session.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def edit_program(request):
    days = ['Day 1', 'Day 2', 'Day 3']
    state = ['true', 'false', 'false']



    context = {"days_state": zip(days, state)}
    return render(request, 'Calendar/editing_calendar.html', context)