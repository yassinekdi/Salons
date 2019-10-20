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
        return {
            'id': message.id,
            'sender': message.sender.slug,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def send_msg(self,message):
        self.send(text_data=json.dumps(message))

    def fetch_messages(self,data):
        pass

    def new_message(self,data):

        sender_slug = data['from']
        sender_account = Account.objects.get(slug=sender_slug)

        message = Message.objects.create(sender=sender_account,
                                         content = data['message'])

        content = {
            'command': 'new_message',
            'message': self.msg_to_json(message)
        }
        return self.send_msg(content)




    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    async def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

