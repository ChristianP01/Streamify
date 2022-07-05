from django.urls import path
from . import views

app_name = "db_operations"

urlpatterns = [
    path("update_db/", views.update_db, name="update_db"),
    path("remove_rece/", views.remove_rece, name="remove_rece")
]