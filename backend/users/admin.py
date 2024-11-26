from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User
# Register your models here.


class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        (_('Avatar'), {'fields': ['avatar']}),
    )

admin.site.register(User, UserAdmin)
