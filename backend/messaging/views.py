import time
from typing import Any

from django.shortcuts import render
import django.utils.translation as translations

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import MessageSerializer, RoomSerializer, LanguageSerializer
from .models import Message, Room, Langauge
from .services import TranslationService

from translation.services import LanguageService

from asgiref.sync import async_to_sync

class MessagesViewSet(viewsets.ModelViewSet):
    translation_service: TranslationService
    language_service: LanguageService
    
    serializer_class= MessageSerializer
    queryset = Message.objects
    permission_classes= [IsAuthenticated]
    
    def __init__(
        self,
        translation_service: TranslationService = TranslationService(),
        language_service: LanguageService = LanguageService(),
        **kwargs: Any
        ) -> None:
        self.language_service = language_service
        self.translation_service = translation_service
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.queryset.filter(room_id = self.kwargs.get('room_pk', 1)).select_related('user')
    
    def filter_queryset(self, queryset):
        messages = super().filter_queryset(queryset)
        try:
            language_code = self.request.language
            async_to_sync(self.translation_service.translate_all)(messages, self.request.user, language_code)
            print('das')
        except Langauge.DoesNotExist as e:
            print(e)
                
        return messages
        
class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes= [IsAuthenticated]
    
class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class= LanguageSerializer
    queryset= Langauge.objects.all()
    permission_classes = [IsAuthenticated]
