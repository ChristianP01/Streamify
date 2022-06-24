from django.shortcuts import render
from streamify.models import Utente, Film, Genere
from django.contrib import messages

def registrati(request):
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
            return render(request,template_name="streamify/home.html", status=409)
            
    # Creo l'utente e lo aggiungo al database
    new_user = Utente(uname, email, pwd, nome, cognome)
    new_user.save()

    messages.success(request, f"Utente creato con successo! Benvenuto, {uname}!")
    return render(request,template_name="streamify/home.html")


def logged(request):
    pwd = request.POST['psw']
    uname = request.POST['uname']

    try:
        logged_user = Utente.objects.filter(username=uname, password=pwd)[0]
        request.session["logged_user"] = logged_user.username

        messages.success(request, f"Benvenuto {request.session['logged_user']}")
        return render(request,template_name="streamify/catalogo.html", context={
            "logged_user": logged_user,
            "film_list": Film.objects.all(),
            "lista_generi": Genere.objects.all()
        }, status=200)

    except:
        messages.error(request, "Credenziali errate!")
        return render(request,template_name="streamify/home.html", status=401)