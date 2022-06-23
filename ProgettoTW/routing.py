from django.urls import path
from .consumers import WSConsumerChatChannels

ws_urlpatterns = [
    path("chatify/chat/<str:room>/", WSConsumerChatChannels.as_asgi())
]