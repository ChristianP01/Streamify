from django.urls import path
from . import views

app_name = "chatify"

urlpatterns = [
    path("chat/<str:room>/", views.chatroom,name="chatroom")
]