from ninja import NinjaAPI
from ninja.security import django_auth

from asgiref.sync import sync_to_async

from .schema import MessageSchema, RoomSchema, UserSchema

from messaging.models import Room

from typing import List

api = NinjaAPI()

@api.get('/rooms', response=List[MessageSchema])
async def list_rooms(request):
    items = await sync_to_async(Room.objects.all)()
    return items