from django.shortcuts import render
from django.views.generic import ListView
from streamify.models import Utente

def homepage(request):
    return render(request,template_name="streamify/home.html")

class listausers(ListView):
    model = Utente
    template_name = "streamify/lista_utenti.html"