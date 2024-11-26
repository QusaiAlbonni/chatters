import json
from typing import Coroutine

from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.exceptions import DenyConnection

from django.contrib.auth.models import AbstractUser

from .models import Room, Message
from .services import AsyncMessagingService, AsyncMessagingAssembler
from .serializers import MessageSerializer
from rest_framework.request import HttpRequest

class ChatConsumer(AsyncJsonWebsocketConsumer):
    room_name: str
    language: str
    room_group_name: str
    room: Room
    user: AbstractUser
    storage_service: AsyncMessagingService
    
    def __init__(self, messaging_service: AsyncMessagingService = AsyncMessagingAssembler(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage_service = messaging_service
        
    async def connect(self):
        self.room_name: str = self.scope["url_route"]["kwargs"].get('room_name', 'global_room')
        self.room_group_name = f"chat_{self.room_name}"
        
        user : AbstractUser = self.scope['user']
        if user.is_anonymous:
            raise DenyConnection("Unauthenticated.")
        
        try:
            self.room = await self.storage_service.get_room_by_name(self.room_name)
        except Room.DoesNotExist:
            raise DenyConnection("Room not found.")
        
        self.user = user
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, json_data):
        message_text = json_data["message"]
        message = await self.storage_service.create_message(user=self.user, room=self.room, content=message_text)
        message_serializer= MessageSerializer(instance=message)
        
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message_serializer.data}
        )

    async def chat_message(self, event):
        message = event["message"]
        print(message)
        await self.send_json({"message": message})
    
    
    