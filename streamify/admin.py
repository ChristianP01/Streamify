from django.contrib import admin
from streamify.models import Film, Genere, Recensione, Utente

admin.site.register(Utente)
admin.site.register(Film)
admin.site.register(Genere)
admin.site.register(Recensione)