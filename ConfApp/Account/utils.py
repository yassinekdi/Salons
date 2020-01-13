from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



def send_general_msg(group_name,msg):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        '{}'.format(group_name),
        {
            'type': 'general_message',
            'title': 'GENERAL MESSAGE',
            'sender': 'from ORGANIZERS',
            'content': msg['content']
        }
    )