from django.urls import path
from . import views

urlpatterns = [
    path('accedi/', views.logged, name="accedi"),
    path('registrati/', views.registrati, name="registrati")
]