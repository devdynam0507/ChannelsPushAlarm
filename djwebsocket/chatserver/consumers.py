from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.channel_name)

        async_to_sync(self.channel_layer.group_add)(
            'test',
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        print("code" +  code)

        async_to_sync(self.channel_layer.group_discard)(
            'test',
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            'test',
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))