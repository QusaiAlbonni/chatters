from django.urls import path
from .api import api


urlpatterns = [
    path('chat/', api.urls)
]
