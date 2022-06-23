from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("streamify/", include("streamify.urls")),
    path("auth/", include("my_auth.urls")),
    path("chatify/", include("chatify.urls"))
]
