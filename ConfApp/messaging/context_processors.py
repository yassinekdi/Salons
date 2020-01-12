from .models import Notification, Notification2
from Account.models import Account
from Conference.models import Conference

def notification(request):

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(notif_user=request.user)
        notifications_count = notifications.filter(notif_read=False).count()
        if notifications_count ==0:
            notifications_count = ''
        return {'notifications': notifications, 'notifications_count': notifications_count}
    return Notification.objects.none()

def notification2(request):

    if request.user.is_authenticated:
        notifications = Notification2.objects.filter(user=request.user)
        notifs_on = [elt for elt in notifications if elt.is_on]

        # switch notifs off
        for notif in notifs_on:
            notif.is_on = False
            notif.save()
        return {'notifications2': notifs_on}


    return Notification2.objects.none()



def user_sessions(request):
    user = request.user
    if request.user.is_authenticated:
        user_sess =  user.reminded_sessions.all()
        return {'user_sessions': user_sess}
    return Account.objects.none()



def user_conf(request):
    try:
        conf = request.user.conferences.all()
    # we suppose that the last one is the one to be accounted for

        if request.user.is_authenticated:
            if len(conf)>0:
                last_conf = conf[len(conf) - 1]
                return {'confs': conf, 'last_conf': last_conf}
    except:
        pass
    return Conference.objects.none()
