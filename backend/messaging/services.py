from messaging.models import Message, Room, Langauge
from .models import Message, Room
from abc import ABC, abstractmethod

from typing import Coroutine, Iterable, Optional
from .models import Message

from django.contrib.auth.models import AbstractUser
from django.conf import settings

from asgiref.sync import sync_to_async

from chatfusion import GeneratorFactory, Prompt

from translation.translator import AITranslator, Translator

from django.contrib.auth import get_user_model

User = get_user_model()

class MessagingService(ABC):
    @abstractmethod
    def create_message(self, **kwargs) -> Message:
        ...

    @abstractmethod
    def creat_room(self, **kwargs) -> Room:
        ...
        
    @abstractmethod
    def get_room_by_name(self, name: str) -> Room:
        ...
        
    @abstractmethod
    def get_room_by_id(self, id: int) -> Room:
        ...
        
        
class AsyncMessagingService(ABC):
    @abstractmethod
    async def create_message(self, **kwargs) -> Message:
        ...

    @abstractmethod
    async def creat_room(self, **kwargs) -> Room:
        ...

    @abstractmethod
    async def get_room_by_name(self, name: str) -> Room:
        ...
    
    @abstractmethod
    async def get_room_by_id(self, id: int) -> Room:
        ...

class AsyncMessagingAssembler(AsyncMessagingService):
    async def create_message(self, **kwargs) -> Message:
        return await Message.objects.select_related('user').acreate(**kwargs)

    async def creat_room(self, **kwargs) -> Room:
        return await Room.objects.acreate(**kwargs)

    async def get_room_by_name(self, name: str) -> Room:
        return await Room.objects.aget(name=name)
    
    async def get_room_by_id(self, id: int) -> Room:
        return await Room.objects.aget(pk=id)
    
class TranslationService():
    translator: Translator
    
    def __init__(self, translator= AITranslator()) -> None:
        self.translator = translator
        
    async def translate_message(
        self, conv: Iterable[Message], message: Message, to: str, source: Optional[str] = None, 
    ) -> str:
        return await self.translator.translate_message(conv, message, to, source)
    
    async def add_translation(self, message: Message, translation: str, lang: str) -> Message:
        """Add a translation to a message."""
        message.translations[lang] = translation
        await message.asave()
        return message

    async def translate_last_message(
        self, messages: Iterable[Message], to: str, source: Optional[str] = None,
    ) -> Message:
        """Translate the last message in a conversation."""
        if not messages:
            raise ValueError("No messages available to translate.")
        
        messages = await sync_to_async(list)(messages)
        last_message = messages[-1]
        translation = await self.translate_message(messages, last_message, source=source, to=to)
        return await self.add_translation(last_message, translation, lang=to)

    async def translate_or_get_last_message(
        self, messages: Iterable[Message], to: str,  source: Optional[str] = None,
    ) -> Message:
        """Translate the last message or return an existing translation if available."""
        messages = await sync_to_async(list)(messages)
        
        if not messages:
            raise ValueError("No messages available to process.")
        
        last_message = messages[-1]

        if to in last_message.translations:
            return last_message

        return await self.translate_last_message(messages, to=to, source=source)
    
    async def translate_last_room_message(
        self,
        room: Room,
        to: str,
        source: str=None,
    ):
        return await self.translate_or_get_last_message(room.messages.all(), to=to, source=source)
    
    async def translate_message_in_room(
        self,
        room: Room,
        message: Message,
        to: str,
        source: str = None,
    ):
        if to in message.translations:
            return message
        
        """Translate a message in a conversation."""
        messages = await sync_to_async(list)(room.messages.prefetch_related('user').all())
        
        if not messages:
            raise ValueError("No messages available to translate.")
        translation = await self.translate_message(messages, message, source=source, to=to)
        return await self.add_translation(message, translation, lang=to)
    
    async def translate_all(self, messages: list[Message], user: User,  to):
        messages = await sync_to_async(list)(messages)
        
        for message in messages:
            if (to in message.translations) or (message.language == to) or (message.user == user):
                continue
            translation = await self.translate_message(messages, message, to=to)
            
            message.translations[to] = translation
        await sync_to_async(Message.objects.bulk_update)(messages, ['translations'])
            
            