import time

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import MessageSerializer, RoomSerializer, LanguageSerializer
from .models import Message, Room, Langauge


class MessagesViewSet(viewsets.ModelViewSet):
    serializer_class= MessageSerializer
    queryset = Message.objects
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(room_id = self.kwargs.get('room_pk', 1))
class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes= [IsAuthenticated]
    
class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class= LanguageSerializer
    queryset= Langauge.objects.all()
    permission_classes = [IsAuthenticated]
