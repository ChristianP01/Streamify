from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('accedi/', views.logged, name="accedi"),
    path('registrati/', views.registrati, name="registrati")
]