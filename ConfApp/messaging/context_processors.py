from .models import Notification
from Account.models import Account

def notification(request):

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(notif_user=request.user)
        notifications_count = notifications.filter(notif_read=False).count()
        if notifications_count ==0:
            notifications_count = ''
        return {'notifications': notifications, 'notifications_count': notifications_count}
    return Notification.objects.none()



def user_sessions(request):
    user = request.user
    if request.user.is_authenticated:
        user_sess =  user.reminded_sessions.all()
        return {'user_sessions': user_sess}
    return Account.objects.none()
