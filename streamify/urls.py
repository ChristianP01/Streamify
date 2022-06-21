from django.urls import path
from . import views

app_name = "streamify"

urlpatterns = [
    path("home/", views.homepage, name="home"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("guarda_film/<str:titolo_film>/", views.guardaFilm, name="guarda_film"),
    path("account/", views.account, name="account"),
    path("review/<str:titolo_film>/", views.review, name="review"),
    path('review_final/', views.review_final, name="review_final"),
    path('cercaFilm/', views.cercaFilm, name="cercaFilm"),
    path("my_reviews/", views.my_reviews, name="my_reviews"),
    path("catalogo_sort/<str:type>/", views.film_sort, name="catalogo_sortup"),
    path("descr_film/<str:titolo_film>/", views.descrizione_film, name="descrizione_film"),
    path("set_preferito/<str:titolo_film>/<str:scelta>/", views.set_preferito, name="set_preferito")
]