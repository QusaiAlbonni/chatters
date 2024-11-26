from ninja import ModelSchema
from users.models import User
from messaging.models import Message, Room

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar',]
        
class MessageSchema(ModelSchema):
    class Meta:
        model = Message
        fields = ['id', 'content', 'translations', 'user', 'room', 'created_at', 'modified_at']
        
class RoomSchema(ModelSchema):
    class Meta:
        model = Room
        fields = ['id', 'name']