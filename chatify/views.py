from django.contrib import messages
from django.shortcuts import render
from streamify.models import Utente

def chatroom(request, room):

    try:
        logged_user = Utente.objects.get(username=request.session["logged_user"])

        return render(request, "chatify/chatpage2.html", context={
            "msg": room,
            "logged_user": logged_user.username
        }, status=200)

    except:
        messages.error(request, "Effettua il login per chattare!")
        return render(request, "streamify/home.html", status=401)