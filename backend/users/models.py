from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(_("Avatar"), upload_to='avatars/', null=True, blank=True)