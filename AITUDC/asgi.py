"""
ASGI config for AITUDC project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from main.middleware import SuperuserWebSocketMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AITUDC.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack

from keytaker.routing import ws_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        SuperuserWebSocketMiddleware(
            URLRouter(ws_urlpatterns)
        )
    ),
})
