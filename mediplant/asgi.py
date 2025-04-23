import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from doctor_visit import routing  # مسیر به فایل routing.py خود

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediplant.settings.prod')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
