# your_project_name/asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from doctor_visit import consumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mediplant.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/<int:doctor_visit_id>/", consumer.ChatConsumer.as_asgi()),  # URL WebSocket
        ])
    ),
})
