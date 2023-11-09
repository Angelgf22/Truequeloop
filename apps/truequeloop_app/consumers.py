import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.datetime_safe import datetime

from .models import Message, OpenChat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['uuid']
        self.room_group_name = f'chat_{self.room_name}'
        # Join
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave chat
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.save_message(text_data_json)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': text_data_json['sender'],
                'timestamp': text_data_json['timestamp']
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timezone.now().isoformat()
        }))

    @sync_to_async
    def save_message(self, message_data):
        sender = self.scope['user']
        receiver = User.objects.get(username=message_data['receiver'])
        uuid = message_data['uuid']
        chat = OpenChat.objects.get(uuid=uuid)
        content = message_data['message']

        Message.objects.create(sender=sender, receiver=receiver, content=content, chat=chat)
