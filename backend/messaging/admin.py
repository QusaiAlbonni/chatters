from django.contrib import admin
from .models import Message, Room, Langauge
# Register your models here.

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Langauge)