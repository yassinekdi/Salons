from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



def which_status(conf,opt):
    res = [conf.superusers, conf.organizers, conf.chairs, conf.speakers]
    return res[opt]

def which_status_user(user,opt):
    res = [user.is_staff, user.is_organizer, user.is_chair, user.is_presenting]
    return res[opt]

def change_status_user(user,opt):
    if opt==0:
        user.is_staff = not user.is_staff
        user.save()
    elif opt==1:
        user.is_organizer = not user.is_organizer
        user.save()
    elif opt==2:
        user.is_chair = not user.is_chair
        user.save()
    elif opt==3:
        user.is_presenting = not user.is_presenting
        user.save()


def send_msg_notif(group_name,notif):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        '{}'.format(group_name),
        {
            'type': 'notif_status',
            'user': notif['user'],
            'content': notif['content'],
            'title': notif['title'],
            'sender': notif['sender']
        }
    )