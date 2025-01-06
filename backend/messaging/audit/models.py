from django.db import models

from messaging.models import Message, Langauge

from django.utils.translation import gettext_lazy as _
# Create your models here.

class PromptLog(models.Model):
    prompt = models.TextField(_("The Prompt used to ask the AI"))
    reply = models.TextField(_("The Reply from the AI"))
    approved = models.BooleanField(_("Whether this response is correct"), default=False)
    message = models.ForeignKey(Message, verbose_name=_("The message being translated"), on_delete=models.SET_NULL, null=True)
    to_language = models.CharField(verbose_name=_("the target language"), max_length=5)

    created_at= models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True, auto_now_add=False)
    
    class Meta:
        ordering = ('approved', 'created_at', 'modified_at')