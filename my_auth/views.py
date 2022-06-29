from django.shortcuts import render
from streamify.models import Utente, Film, Genere
from django.contrib import messages

def registrati(request):
    username = request.POST['username']
    pwd = request.POST['password']
    email = request.POST['email']
    nome = request.POST['nome']
    cognome = request.POST['cognome']

    # Controllo se l'utente esiste già
    utenti = Utente.objects.all()
    for utente in utenti:
        if utente.username == username:
            messages.add_message(request, messages.ERROR, "Username già in uso!")
            return render(request,template_name="streamify/home.html", status=409)
            
    # Creo l'utente e lo aggiungo al database
    new_user = Utente(username, email, pwd, nome, cognome)
    new_user.save()

    messages.add_message(request, messages.SUCCESS, f"Utente creato con successo! Benvenuto, {new_user.username}!")
    return render(request,template_name="streamify/home.html")


def logged(request):
    pwd = request.POST['password']
    username = request.POST['username']

    try:
        logged_user = Utente.objects.filter(username=username, password=pwd)[0]
        request.session["logged_user"] = logged_user.username

        messages.add_message(request, messages.SUCCESS, f"Benvenuto {request.session['logged_user']}")
        return render(request,template_name="streamify/catalogo.html", context={
            "logged_user": logged_user,
            "film_list": Film.objects.all(),
            "lista_generi": Genere.objects.all()
        }, status=200)

    except:
        messages.add_message(request, messages.ERROR, "Credenziali errate!")
        return render(request,template_name="streamify/home.html", status=401)