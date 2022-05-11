from django.shortcuts import render
from django.views.generic import ListView
from streamify.models import Film, Utente

def homepage(request):
    return render(request,template_name="streamify/home.html")

class listausers(ListView):
    model = Utente
    template_name = "streamify/lista_utenti.html"

def registrato(request):
    uname = request.POST['uname']
    pwd = request.POST['psw']
    email = request.POST['email']

    new_user = Utente(uname, email, pwd)
    new_user.save()


    return render(request,template_name="streamify/registrato.html", context={
        "user": uname,
        "pass": pwd,
        "email": email
    })

def logged(request):
    pwd = request.POST['psw']
    uname = request.POST['uname']

    try:
        logged_user = Utente.objects.get(username=uname, password=pwd)
        print(Utente.objects.all())
        return render(request,template_name="streamify/logged.html", context={
            "user": uname,
            "pass": pwd
        })

    except:
        return render(request,template_name="streamify/log_failed.html")

class mostra_catalogo(ListView):
    model = Film
    template_name = "streamify/catalogue.html"