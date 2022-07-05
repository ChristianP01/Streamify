from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from streamify.models import Film, Recensione
from django.contrib import messages

@require_GET
@login_required
def update_db(request):

    titolo_film = request.GET['titolo_film']
    nuovo_voto = request.GET['nuovo_voto']
    nuovo_commento = request.GET['nuovo_commento']
    
    if int(nuovo_voto) > 5:
        nuovo_voto = '5'

    if int(nuovo_voto) < 1:
        nuovo_voto = '1'

    rece_updated = Recensione.objects.get(film=Film.objects.get(titolo=titolo_film), utente=request.user)
    rece_updated.voto = nuovo_voto
    rece_updated.commento_scritto = nuovo_commento
    rece_updated.save()

    messages.add_message(request, messages.SUCCESS, "Recensione modificata con successo!")
    return render(request, template_name="account.html", context={
        "logged_user": request.user
    }, status=200)



@require_GET
@login_required
def remove_rece(request):

    titolo_film = request.GET['titolo_film']
    Recensione.objects.get(film=Film.objects.get(titolo=titolo_film), utente=request.user).delete()

    messages.add_message(request, messages.SUCCESS, "Recensione eliminata con successo!")
    return render(request, template_name="account.html", context={
        "logged_user": request.user
    }, status=200)