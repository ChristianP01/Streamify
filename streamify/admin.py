from django.contrib import admin
from streamify.models import Film, Genere, Utente

admin.site.register(Utente)
admin.site.register(Film)
admin.site.register(Genere)