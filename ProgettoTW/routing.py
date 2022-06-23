from django.urls import path
from .consumers import WSConsumerChat, WSConsumerChatChannels

ws_urlpatterns = [
    path("chatify/chatws/", WSConsumerChat.as_asgi()),
    path("chatify/chatws/<str:room>/", WSConsumerChatChannels.as_asgi())
]