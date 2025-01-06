from django.contrib import admin
from .models import PromptLog

# Register your models here.

@admin.register(PromptLog)
class PromptLogAdmin(admin.ModelAdmin):
    list_filter= ('approved', 'created_at', 'modified_at')