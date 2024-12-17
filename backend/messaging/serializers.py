from rest_framework import serializers
from .models import Message, Room
from users.serializers import UserSerializer
class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = [
            'pk',
            'content',
            'language',
            'translations',
            'user',
            'room',
            'created_at',
            'modified_at'
        ]
        
        
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'pk',
            'name',
        ]