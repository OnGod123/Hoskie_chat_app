import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import CustomUser, Room
from channels.db import database_sync_to_async

class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'chat_{self.username}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']

        if message_type in ['offer', 'answer', 'candidate', 'message']:
            recipient_username = data.get('recipient')
            recipient_group_name = f'chat_{recipient_username}'
            await self.channel_layer.group_send(
                recipient_group_name,
                {
                    'type': 'webrtc_message',
                    'message': data
                }
            )

    async def webrtc_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def store_message(self, data):
        sender = CustomUser.objects.get(username=self.sender_username)
        recipient = CustomUser.objects.get(username=self.recipient_username)
        room, created = Room.objects.get_or_create(name=self.room_name)
        if created:
            room.participants.add(sender, recipient)
        Message.objects.create(
            room=room,
            sender=sender,
            recipient=recipient,
            content=data['message']
        )
