from django.contrib import messages
from django.shortcuts import render
from streamify.models import Film, Genere
from django.views.decorators.http import require_safe
from django.contrib.auth.decorators import login_required

@require_safe
@login_required
def chatroom(request, room):

    logged_user = request.user
    
    try:
        # Controllo se l'utente loggato ha guardato il film, prima di entrare nella chat.
        # Room contiene il titolo del film
        logged_user.film_guardati.get(titolo=room)

    except Film.DoesNotExist:
        messages.error(request, "Devi aver guardato il film per chattare!")
        return render(request, "streamify/catalogo.html", context={
            "film_list": Film.objects.all(),
            "logged_user": logged_user,
            "lista_generi": Genere.objects.all()
        }, status=401)

    return render(request, "chatify/chat_page.html", context={
        "msg": room,
        "logged_user": logged_user
    }, status=200)