import json
from channels.generic.websocket import AsyncWebsocketConsumer

messages_list = []
class WSConsumerChat(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send("[Server]: Connessione effettuata!")


    async def receive(self, text_data=None, bytes_data=None):
        if text_data == "UPDATE":
            stot = ""
            for m in messages_list:
                stot += m["user"] + ": " + m["msg"] + "\n"

            await self.send(stot)

        else:
            if text_data != None:
                messages_list.append(json.loads(text_data))

        if len(messages_list) > 20:
            messages_list.clear()


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

