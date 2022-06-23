from django.urls import path
from . import views

app_name = "chatify"

urlpatterns = [
    path("chatws/", views.chatws, name="chatws"),
    path("<str:room>/", views.chatroom,name="chatroom")
]