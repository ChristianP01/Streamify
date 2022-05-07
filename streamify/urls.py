from django.urls import path
from . import views

app_name = "streamify"

urlpatterns = [
    path("home/", views.homepage, name="home"),
    path("listausers/", views.listausers.as_view(), name="listausers")
]
