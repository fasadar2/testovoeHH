from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/mail/', consumers.MailConsumer.as_asgi()),
    path('ws/get-mail/',consumers.MailFromDbConsumer.as_asgi())
]