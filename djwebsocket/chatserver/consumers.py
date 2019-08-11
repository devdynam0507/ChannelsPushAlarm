from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import json

single_channels = {}

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

"""
Realtime alarm
"""
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']

        # 인증이 안된 유저면 return
        if user.is_anonymous:
            return

        if is_superuser(user):
            await get_channel_layer().group_add(
                'admin-alarm',
                self.channel_name
            )
        else:
            single_channels[user.username] = self.channel_name # 일반 유저들은 싱글채널에 저장됩니다.

        await self.accept()

    async def disconnect(self, code):
        user = self.scope['user']

        if is_superuser(user):
            await get_channel_layer().group_discard(
                'admin-alarm',
                self.channel_name
            )
        elif not user.is_anonymous:
            del single_channels[user]

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = self.scope['user']
        message = text_data_json['message']

        if is_superuser(user) and 'receiver' not in text_data_json:
            await get_channel_layer().group_send(
                'admin-alarm',
                {
                    'type': 'admin_alarm_handler',
                    'message': message
                }
            )
        elif not user.is_anonymous and 'receiver' in text_data_json:
            receiver = text_data_json['receiver']
            channel_name = single_channels[receiver]
            await get_channel_layer().send(channel_name, {
                'type': 'user_push_alarm_handler',
            })

    async def user_push_alarm_handler(self, event):
        await self.send(text_data=json.dumps({
            'message': "문의에 대한 답변이 도착했습니다."
        }))

    async def admin_alarm_handler(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))