from .models import Notification

def notification(request):

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(notification_user=request.user)
        notifications_count = Notification.objects.filter(notification_read=True).count()
        if notifications_count ==0:
            notifications_count = ''
        return {'notifications': notifications, 'notifications_count': notifications_count}
    return Notification.objects.none()


