from messaging.models import Message, Room
from .models import Message, Room
from abc import ABC, abstractmethod

from typing import Coroutine

from django.contrib.auth.models import AbstractUser

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

class AsyncMessagingAssembler(AsyncMessagingService):
    async def create_message(self, **kwargs) -> Message:
        return await Message.objects.select_related('user').acreate(**kwargs)

    async def creat_room(self, **kwargs) -> Room:
        return await Room.objects.acreate(**kwargs)

    async def get_room_by_name(self, name: str) -> Room:
        return await Room.objects.aget(name=name)