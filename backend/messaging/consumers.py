import json
from typing import Coroutine, Literal

from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.exceptions import DenyConnection

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from users.models import User

from .models import Room, Message
from .services import AsyncMessagingService, AsyncMessagingAssembler, AITranslationService, TranslationService
from .serializers import MessageSerializer
from rest_framework.request import HttpRequest
from urllib.parse import parse_qs

from .utils import detect_message_lang, detect_lang

langs = settings.SUPPORTED_LANGUAGES

class ChatConsumer(AsyncJsonWebsocketConsumer):
    room_name: str
    language: str
    room_group_name: str
    room: Room
    user: AbstractUser
    storage_service: AsyncMessagingService
    translate_service: TranslationService
    
    def __init__(self, messaging_service: AsyncMessagingService = AsyncMessagingAssembler(), translate_service: TranslationService = AITranslationService(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage_service = messaging_service
        self.translate_service= translate_service
        
    async def connect(self):
        self.room_name: str = self.scope["url_route"]["kwargs"].get('room_name', 'global_room')
        self.room_group_name = f"chat_{self.room_name}"
        
        query_string = self.scope.get("query_string", b"").decode()
        query_dict = parse_qs(query_string)
        self.language= query_dict.get('lang', None)[0]
        
        if self.language not in langs:
            raise DenyConnection("Unsoppurted Language")
        
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
        language = await detect_lang(message_text)
        message = await self.storage_service.create_message(user=self.user, room=self.room, content=message_text, language=language)
        message_serializer= MessageSerializer(instance=message)
        
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message_serializer.data}
        )

    async def chat_message(self, event):
        message = event["message"]
        if (message['language'] != self.language) and self.language and not (message['user']['id'] == self.user.id):
            print(message)
            user = await User.objects.aget(pk=message['user']['id'])
            message_obj = Message(
                id= message['pk'],
                user=user,
                room=self.room,
                content=message['content'],
                language=message['language'],
                translations=message['translations'],
                created_at=message['created_at'],
                modified_at=message['modified_at']
            )
            message_obj.user= user
            message_obj = await self.translate_service.translate_message_in_room(room=self.room, message=message_obj, to=self.language)
            message['translations'] = message_obj.translations
            
        await self.send_json({"message": message})
    
    
    