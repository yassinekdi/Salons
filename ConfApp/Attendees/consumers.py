from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
from Conference.models import Conference

# The notif is sent from views.py of ATTENDEES > Finds a connection with the same group name > fires the function
# with the same name notif_status
class Notifs(AsyncJsonWebsocketConsumer):



    async def connect(self):
        user = self.scope['user']

        if user.is_anonymous:
            await self.close()
        else:
            # -----  Group of status modification   ------
            group_status= "notif_status"
            await self.channel_layer.group_add(
                group_status,
                self.channel_name
            )

            # -----  Group of XXXXXX   ------
            # self.status_notif_group= "Notif_status_conf"+str(this_conf.id)
            #
            # await self.channel_layer.group_add(
            #     self.status_notif_group,
            #     self.channel_name
            # )

            await self.accept()





    async def receive(self, content):
        print('CONSUMERS ---- RECEIVE FUNCTION')
        pass
        # command = content.get("command", None)
        # try:
        #     if command == "join":
        #         await self.join_room(content['room'])
        #     elif command == "leave":
        #         await self.leave_room(content['room'])
        #     elif command == "send":
        #         await self.send_room(content['room'], content['message'])
        # except:
        #     print('ClientError part')



    async def disconnect(self, close_code):
        pass
        #     try:
        #         await self.leave_room(room_id)
        #     except:
        #         print('ClientError + pass')
        #         pass

# Command helper methods called in receive function

    async def notif_status(self,event):
        user = self.scope['user']

        if str(user.id) == event['user']:
            await self.send_json(
                {
                    'type': 'notif_status',
                    'content': event
                }
            )

    # async def join_room(self, room_id):
    #     room = await get_room_or_error(room_id, self.scope['user'])
    #     # Send join message if it's turned on
    #     if settings.NOTIFYXX:
    #         await self.channel_layer.group_send(
    #             room.group_name,
    #             {
    #                 "type": "chat.join",
    #                 "room_id": room_id,
    #                 "username": self.scope['user'].username,
    #             }
    #         )
    #
    #     # Store that we're in room
    #     self.rooms.add(room_id)
    #
    #     # add them to the group so they get room msgs
    #     await self.channel_layer.gro





#utils functions
