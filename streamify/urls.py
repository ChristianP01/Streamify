from django.urls import path
from . import views

app_name = "streamify"

urlpatterns = [
    path("home/", views.homepage, name="home"),
    path("registrato/", views.registrato, name="registrato"),
    path("logged/", views.logged, name="logged"),
    path("catalogo/", views.mostra_catalogo.as_view(), name="catalogo"),
    path("guarda_film/<str:titolo_film>/", views.guardaFilm, name="guarda_film"),
    path("account/", views.account, name="account"),
    path("review/<str:titolo_film>/", views.review, name="review"),
    path('review_final/', views.review_final, name="review_final"),
    path('cercaFilm/', views.cercaFilm, name="cercaFilm")
]
