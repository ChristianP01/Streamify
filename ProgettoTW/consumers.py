import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WSConsumerChatChannels(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = 'chat_' + self.room_name

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json['user']
        message = text_data_json['msg']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'msg': message,
                'user': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['msg']
        username = event['user']

        await self.send(text_data=json.dumps({
            'msg': message,
            'user': username,
        }))

