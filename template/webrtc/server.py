import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser  # Import for user handling

class SignalingConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'signaling_{self.room_name}'

    # Get user from request (replace with your authentication logic)
    self.user = self.scope['user'] if self.scope['user'].is_authenticated else AnonymousUser()

    # Check user access to the room (replace with your authorization logic)
    if not self.user.has_perm('access_room', self.room_name):
      await self.close(code=403)  # Forbidden access

    # Join room group
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()

  async def disconnect(self, close_code):
    # Leave room group
    await self.channel_layer.group_discard

