from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Room(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    
    created_at= models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True, auto_now_add=False)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('created_at',)

def get_default_room() -> Room:
    return Room.objects.get_or_create(name='global')[0].id


class Message(models.Model):
    content = models.TextField(_("Message Content"), max_length=4096)
    user = models.ForeignKey(User, related_name='messages', verbose_name=_("User"), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='messages', verbose_name=_("Room"), on_delete=models.CASCADE, default=get_default_room)
        
    translations= models.JSONField(_("Translations"), default=dict)
    
    language= models.CharField(_("Content Language"), max_length=31)
    
    created_at= models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True, auto_now_add=False)
    
    def __str__(self) -> str:
        return str(self.pk) + "-" + self.content[:100]

    class Meta:
        ordering= ('created_at',)


class Langauge(models.Model):
    code= models.CharField(_("The id of the Language"), max_length=15, unique=True)
    
    name = models.CharField(_("The verbose name of the Language"), max_length=127)
    
    class Meta:
        ordering = ('code', 'name')