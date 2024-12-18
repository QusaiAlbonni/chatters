"""
ASGI config for chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

django_asgi_app = get_asgi_application()

from messaging.routing import websocket_urlpatterns
from messaging.middleware import TokenAuthMiddleware

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": 
            AllowedHostsOriginValidator(
                TokenAuthMiddleware(
                    AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
                )
            ),
    }
)
