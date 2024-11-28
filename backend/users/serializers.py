from rest_framework import serializers
from djoser.serializers import UserSerializer as DjUserSerializer, UserCreateSerializer as DjUserCreateSerializer
from .models import User

class UserSerializer(DjUserSerializer):
    class Meta:
        ref_name='users'
        model = User
        fields = DjUserSerializer.Meta.fields + ('avatar', 'id')
        read_only_fields = DjUserSerializer.Meta.read_only_fields + ('avatar', 'id')
        
class UserCreateSerializer(DjUserCreateSerializer):
    class Meta(DjUserCreateSerializer.Meta):
        fields = DjUserCreateSerializer.Meta.fields + (
            'avatar',
        )