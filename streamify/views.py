from email import message
import json
import pprint
from re import template
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from streamify.models import Film, Recensione, Utente, Genere
from django.contrib import messages
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def homepage(request):
    return render(request,template_name="streamify/home.html")

class listausers(ListView):
    model = Utente
    template_name = "streamify/lista_utenti.html"

def registrato(request):
    uname = request.POST['uname']
    pwd = request.POST['psw']
    email = request.POST['email']
    nome = request.POST['nome']
    cognome = request.POST['cognome']

    # Controllo se l'utente esiste già
    utenti = Utente.objects.all()
    for utente in utenti:
        if utente.username == uname:
            messages.error(request, "Username già in uso!")
            return render(request,template_name="streamify/home.html")
            
    # Creo l'utente e lo aggiungo al gruppo dei loggati.
    new_user = Utente(uname, email, pwd, nome, cognome)
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
        return render(request,template_name="streamify/catalogo.html", context={
            "logged_user": logged_user,
            "film_list": film_list
        })

    except:
        messages.error(request, "Credenziali errate!")
        return render(request,template_name="streamify/home.html")

class mostra_catalogo(ListView):
    model = Film
    template_name = "streamify/catalogo.html"


def guardaFilm(request, titolo_film):

    #Se un utente prova a guardare un film senza essere loggato (ad esempio scrivendo direttamente l'URL del film
    # oppure i cookie della sessione scadono, ritorno None come utente per avvisare l'utente di effettuare il login.)
    try:
        logged_user = request.session["logged_user"]
    except:
        logged_user = None

    for film in Film.objects.all():
        if logged_user is not None and titolo_film == film.titolo:
            
            #Update del DB
            Utente.objects.filter(username=logged_user)[0].film_guardati.add(Film.objects.filter(titolo=titolo_film)[0])

            return render(request,template_name="streamify/catalogo.html", context={
                "film_list": Film.objects.all(),
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
        for utente in Utente.objects.all():
            if user == utente.username:

                generi = {}

                # TODO: Ottimizzare questo
                # Creo il dizionario con la sintassi {genere: numero_di_film_guardati_di_quel_genere}
                # Questo mi serve per disegnare il grafico e gestire il recommendation system
                for film in utente.film_guardati.all():
                    for genere in film.generi.all():
                        if genere.name not in generi:
                            generi[genere.name] = 1
                        else:
                            generi[genere.name] += 1

                for genere in Genere.objects.all():
                    if genere.name not in generi:
                        generi[genere.name] = 0

                # Mi salvo un riferimento alla lista dei generi, in modo da poterla ricaricare in futuro (review)
                request.session["generi"] = generi
                

                return render(request, template_name="streamify/account.html", context={
                    "logged_user": user,
                    "lista_film": utente.film_guardati.all(),
                    "generi_dict": json.dumps(generi)
                })

    except:
        return render(request, template_name="streamify/account.html", context={
        "logged_user": None,
        "lista_film": None
    })

def review(request):

    try:

        value = request.POST["selected_star"]
        film = request.POST["selected_film"]
        user = Utente.objects.get(username=request.session["logged_user"])

        print(f"Recensione con voto {value} per {film}")
        
        # Creo una nuova recensione, scritta dall'utente loggato per il film selezionato
        new_rece = Recensione(value, user, film, "")
        new_rece.save()

        return render(request, template_name="account.html")
    
    except:
        return render(request, template_name="account.html", context={
            "logged_user": user,
            "lista_film": user.film_guardati.all(),
            "generi_dict": json.dumps(request.session["generi"])
        })