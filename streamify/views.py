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
            
    # Creo l'utente e lo aggiungo al database
    new_user = Utente(uname, email, pwd, nome, cognome)
    new_user.save()

    messages.success(request, f"Utente creato con successo! Benvenuto, {uname}!")
    return render(request,template_name="streamify/home.html")

def logged(request):
    pwd = request.POST['psw']
    uname = request.POST['uname']

    try:
        logged_user = Utente.objects.get(username=uname, password=pwd)
        
        request.session["logged_user"] = logged_user.username

        messages.success(request, f"Benvenuto {request.session['logged_user']}")
        return render(request,template_name="streamify/catalogo.html", context={
            "logged_user": logged_user,
            "film_list": Film.objects.all(),
            "query_film": None
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

        for film in Film.objects.all():
            if logged_user is not None and titolo_film == film.titolo:
                
                #Update del DB
                Utente.objects.filter(username=logged_user)[0].film_guardati.add(Film.objects.filter(titolo=titolo_film)[0])

                messages.success(request, f"{titolo_film} guardato con successo!")
                return render(request,template_name="streamify/catalogo.html", context={
                    "film_list": Film.objects.all(),
                    "logged_user": logged_user,
                    "query_film": None
                })

    except:

        messages.error(request, "Effettua il login per guardare il film!")
        return render(request, template_name="home.html")

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

def review(request, titolo_film):

    try:

        user = Utente.objects.get(username=request.session["logged_user"])
        film = Film.objects.get(titolo=titolo_film)
        request.session["film"] = film.titolo

        return render(request, template_name="review.html", context={
            "logged_user": user,
            "film": film
            })
    
    except:
        messages.error(request, "Effettua il login per lasciare una recensione!")
        return render(request, template_name="home.html", context={
            "logged_user": None,
            "lista_film": None
        })
        

def review_final(request):

    try:

        value = request.POST["selected_star"]
        film = Film.objects.get(titolo=request.session["film"])
        user = Utente.objects.get(username=request.session["logged_user"])

        if Recensione.objects.get(utente=user, film=film):
            messages.error(request, "Hai già recensito questo film!")
            return render(request, template_name="account.html", context={
                "logged_user": user,
                "lista_film": user.film_guardati.all(),
                "generi_dict": json.dumps(request.session["generi"])
            })

        new_rece = Recensione(voto=value, utente=user, film=film, commento_scritto="Commento_Di_Prova")
        new_rece.save()

        messages.success(request, "Hai recensito correttamente il film!")
        return render(request, template_name="account.html", context={
            "logged_user": user,
            "lista_film": user.film_guardati.all(),
            "generi_dict": json.dumps(request.session["generi"])
        })

    except:
        messages.error(request, "Effettua il login per lasciare una recensione!")
        return render(request, template_name="home.html")


def cercaFilm(request):

    # Non c'è bisogno di controllare l'utente loggato perchè chiunque dovrebbe poter cercare nel catalogo.

    user_input = request.POST["film_search"]
    logged_user = request.session["logged_user"]

    film_query = Film.objects.filter(titolo__startswith=user_input)

    return render(request,template_name="streamify/catalogo.html", context={
        "logged_user": logged_user,
        "film_list": film_query,
        "query_film": None
    })