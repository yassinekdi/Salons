from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Discussion, Notification
from Account.models import Account
import json
from django.shortcuts import get_object_or_404

# def get_current_discussion(discussionId):
#     return get_object_or_404(Discussion, id=discussionId)



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['disc_slug']
        self.room_group_name = 'chat_%s' % self.room_name


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def many_msg_to_json(self,messages):
        result = []
        for msg in messages:
            result.append(self.msg_to_json(msg))

        return result

    def msg_to_json(self, message):
        msg_time = message.timestamp
        hour,minute,month,day = msg_time.hour,msg_time.minute, msg_time.strftime('%b'),msg_time.day
        msg_time_str = str(hour) +':'+str(minute)+' ' + ' | ' + month + ' '+ str(day)
        return {
            'id': message.id,
            'sender': message.sender.slug,
            'content': message.content,
            'timestamp': msg_time_str
        }





    def old_messages(self,data):

        discussion_slug = Discussion.objects.get(slug=data['discussion_slug'])
        last_msgs = discussion_slug.messages.all()[:15]
        content = {
            'command': 'old',
            'message': self.many_msg_to_json(last_msgs)
        }
        return content



    def new_message(self,data):

        sender_slug = data['from']
        sender_account = Account.objects.get_or_create(slug=sender_slug)[0]
        print('sender account', sender_account)
        current_discussion = Discussion.objects.get(slug=data['discussion_slug'])
        print('CURRENT DISCUSSION', current_discussion)
        receiver = [int(elt) for elt in data['discussion_slug'].split('n')[1:] if int(elt) != sender_account.id][0]
        receiver_account = Account.objects.get(id=receiver)


        new_msg = Message.objects.create(sender=sender_account,
                                         content = data['message'],
                                         discussion = current_discussion)


        notification_sender = Notification.objects.get_or_create(notif_user=sender_account,
                                                                 notif_discussion=data['discussion_slug'],)[0]
        notification_sender.notif_read = True
        notification_sender.save()
        # print('NOTIF SENDER ID', notification_sender.id)
        # print('NOTIF SENDER READ', notification_sender.notif_read)
        # Can be done using signals: Creating notification after creating msgs
        notification_receiver = Notification.objects.get_or_create(notif_user=receiver_account,
                                                          notif_discussion=data['discussion_slug'])[0]
        notification_receiver.notif_read=False
        notification_receiver.save()
        print('NOTIF RECEIVER ID', notification_receiver.id)


        content = {
            'command': 'new_message',
            'message': self.msg_to_json(new_msg),
            #'notif': self.notif_to_json(notification_receiver)
        }


        return content

    commands = {
        'old_messages': old_messages,
        'new_message': new_message,
        #'notif_to_false': notif_to_false
    }

    async def receive(self, text_data):
        data = json.loads(text_data)

        content = self.commands[data['command']](self,data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content
            }
        )




    async def chat_message(self, event):
        print('RECEIVED SOMTHING')
        content = event["message"]


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': content,

        }))

