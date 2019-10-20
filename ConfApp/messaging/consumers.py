from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from Account.models import Account
import json
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
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

    def msg_to_json(self, message):
        msg_time = message.timestamp
        hour,minute,am_pm,month,day = msg_time.hour,msg_time.minute,msg_time.strftime('%p'),\
                                      msg_time.strftime('%b'),msg_time.day
        msg_time_str = str(hour) +':'+str(minute)+' '+ am_pm + ' | ' + month + ' '+ str(day)
        return {
            'id': message.id,
            'sender': message.sender.slug,
            'content': message.content,
            'timestamp': msg_time_str
        }



    def fetch_messages(self,data):
        pass

    def new_message(self,data):

        sender_slug = data['from']
        sender_account = Account.objects.get(slug=sender_slug)

        new_msg = Message.objects.create(sender=sender_account,
                                         content = data['message'])
        content = {
            'command': 'new_message',
            'message': self.msg_to_json(new_msg)
        }
        return content

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
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
        content = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': content
        }))

