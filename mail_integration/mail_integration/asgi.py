import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import mail.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mail_integration.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mail.routing.websocket_urlpatterns
        )
    ),
})