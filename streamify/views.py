from email import message
from django.shortcuts import render
from django.views.generic import ListView
from streamify.models import Film, Utente
from django.contrib import messages

def homepage(request):
    return render(request,template_name="streamify/home.html")

class listausers(ListView):
    model = Utente
    template_name = "streamify/lista_utenti.html"

def registrato(request):
    uname = request.POST['uname']
    pwd = request.POST['psw']
    email = request.POST['email']

    # Controllo se l'utente esiste già
    utenti = Utente.objects.all()
    for utente in utenti:
        if utente.username == uname:
            messages.error(request, "Username già in uso!")
            return render(request,template_name="streamify/home.html")
            
    new_user = Utente(uname, email, pwd)
    new_user.save()

    messages.success(request, f"Utente creato con successo! Benvenuto, {uname}!")
    return render(request,template_name="streamify/home.html")

def logged(request):
    pwd = request.POST['psw']
    uname = request.POST['uname']

    try:
        logged_user = Utente.objects.get(username=uname, password=pwd)
        film_list = Film.objects.all()
        request.session["logged_user"] = logged_user.username
        return render(request,template_name="streamify/catalogue.html", context={
            "logged_user": logged_user,
            "film_list": film_list
        })

    except:
        messages.error(request, "Credenziali errate!")
        return render(request,template_name="streamify/home.html")

class mostra_catalogo(ListView):
    model = Film
    template_name = "streamify/catalogue.html"


def guardaFilm(request, titolo):

    lista_film = Film.objects.all()

    #Se un utente prova a guardare un film senza essere loggato (ad esempio scrivendo direttamente l'URL del film
    # oppure i cookie della sessione scadono, ritorno None come utente per avvisare l'utente di effettuare il login.)
    try:
        logged_user = request.session["logged_user"]
    except:
        logged_user = None

    for film in lista_film:
        if titolo == film.titolo:
            return render(request,template_name="streamify/guarda_ora.html", context={
                "film": film,
                "logged_user": logged_user
            })

    return render(request, template_name="streamify/guarda_ora.html", context={
        "film": None    
    })

def account(request):

    # Non posso fare entrare un utente in questa pagina se non è loggato, quindi ritorno None.
    try:
        user = request.session["logged_user"]
        # Se l'utente è entrato correttamente, lo cerco nel database al fine di ottenere i film che ha guardato.
        utenti = Utente.objects.all()
        print(utenti)
        for utente in utenti:
            if user == utente.username:
                return render(request, template_name="streamify/account.html", context={
                    "user": user,
                    "lista_film": utente.film_guardati.all()
                })

    except:
        return render(request, template_name="streamify/account.html", context={
        "user": None,
        "lista_film": None
    })

    