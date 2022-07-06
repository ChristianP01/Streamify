import json
from django.shortcuts import render
from streamify.models import Film, Recensione, Genere
from streamify.methods import calcola_generi, calcola_recommendation_system
from django.contrib import messages
from django.views.decorators.http import require_safe, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@require_safe
def homepage(request):

    # Resetto request.session in modo da simulare un logout completo.
    request.session.clear()

    # Logout dell'user (in caso fosse loggato), altrimenti l'esecuzione procede senza errori.
    logout(request)

    return render(request,template_name="streamify/home.html")


@require_safe
def catalogo(request):
    # Qui ci entrerà un utente guest oppure dopo aver cliccato "Reset" nei filtri del catalogo

    return render(request,template_name="streamify/catalogo.html", context={
            "logged_user": request.user,
            "film_list": Film.objects.all(),
            "lista_generi": Genere.objects.all()
        }, status=200)


@require_safe
@login_required
def guarda_film(request, titolo_film):

    logged_user = request.user

    if Film.objects.get(titolo=titolo_film) not in logged_user.film_guardati.all():

        #Update del DB se l'utente non ha ancora guardato il film
        logged_user.film_guardati.add(Film.objects.get(titolo=titolo_film))

        messages.add_message(request, messages.SUCCESS, f"{titolo_film} guardato con successo!")
        return render(request,template_name="streamify/catalogo.html", context={
            "film_list": Film.objects.all(),
            "logged_user": logged_user,
            "lista_generi": Genere.objects.all()
        }, status=200)

    # Se invece l'ha già guardato
    else:
        messages.add_message(request, messages.WARNING, f"Hai già guardato {titolo_film}!")
        return render(request,template_name="streamify/catalogo.html", context={
            "film_list": Film.objects.all(),
            "logged_user": logged_user,
            "lista_generi": Genere.objects.all()
        }, status=409)


@require_safe
@login_required
def account(request):

    return render(request, template_name="streamify/account.html", context={
        "logged_user": request.user,
        "generi_dict": json.dumps(calcola_generi(request.user)),
        "recommended_films": calcola_recommendation_system(request.user)
    }, status=200)
    

@require_safe
@login_required
def review(request, titolo_film):
    
    film = Film.objects.get(titolo=titolo_film)
    request.session["film"] = film.titolo

    return render(request, template_name="review.html", context={
        "logged_user": request.user,
        "film": film,
        "lista_recensioni": Recensione.objects.filter(film=film)
    }, status=200)
        

@require_POST
@login_required
def review_final(request):

    if request.POST["selected_star"].isnumeric():
        value = int(request.POST["selected_star"])

    else:
        messages.add_message(request, messages.ERROR, "Devi inserire una valutazione corretta!")
        return render(request, template_name="streamify/review.html", context={
            "logged_user": request.user,
            "film": Film.objects.get(titolo=request.session["film"]),
            "lista_recensioni": Recensione.objects.filter(film=Film.objects.get(titolo=request.session["film"]))
        }, status=206)
        
    commento_scritto = request.POST["commento_scritto"]

    film = Film.objects.get(titolo=request.session["film"])
    logged_user = request.user

    if len(Recensione.objects.filter(utente=logged_user, film=film)) == 0:
        new_rece = Recensione(voto=value, utente=logged_user, film=film, commento_scritto=commento_scritto)
        new_rece.save()

        messages.add_message(request, messages.SUCCESS, "Hai recensito correttamente il film!")
        return render(request, template_name="account.html", context={
            "logged_user": logged_user,
            "generi_dict": json.dumps(calcola_generi(request.user)),
            "recommended_films": calcola_recommendation_system(request.user)
        }, status=200)


    else:
        messages.add_message(request, messages.WARNING, "Hai già recensito questo film!")
        return render(request, template_name="account.html", context={
            "logged_user": logged_user,
            "generi_dict": json.dumps(calcola_generi(request.user)),
            "recommended_films": calcola_recommendation_system(request.user)
        }, status=409)



@require_POST
def cerca_film(request):

    logged_user = request.user

    user_input = request.POST["film_search_title"]
    genre_input = request.POST["generi"]
    min_score = request.POST["min_score"]
    max_score = request.POST["max_score"]

    try:
        1 + float(min_score)
        min_score = float(min_score)
    except ValueError:
        min_score = 1.0

    try:
        1 + float(max_score)
        max_score = float(max_score)
    except ValueError:
        max_score = 5.0

    film_query = Film.objects.filter(titolo__startswith=user_input, generi__name__startswith=genre_input).distinct()
    
    # Ho bisogno di un'altra lista perchè non posso rimuovere elementi da un QuerySet.
    film_query_matched = []
    for film in film_query:
        if film.get_mediavoto() >= min_score and film.get_mediavoto() <= max_score:
            film_query_matched.append(film)
                
    return render(request,template_name="streamify/catalogo.html", context={
        "logged_user": logged_user,
        "film_list": film_query_matched,
        "lista_generi": Genere.objects.all()
    }, status=200)


@require_safe
@login_required
def my_reviews(request):

    logged_user = request.user

    return render(request,template_name="streamify/user_reviews.html", context={
        "film_list": logged_user.film_guardati.all(),
        "lista_recensioni": Recensione.objects.filter(utente=logged_user)
    }, status=200)



@require_GET
def film_sort(request, sort_type):
    # sort_type = {up | down} in base al tipo di sorting richiesto.

    if sort_type == "up":
        sort_type = True
    else:
        sort_type = False

    return render(request,template_name="streamify/catalogo.html", context={
        'logged_user': request.user,
        "film_list": sorted(Film.objects.all(), key= lambda film: film.get_mediavoto(), reverse=sort_type),
        "lista_generi": Genere.objects.all()
    }, status=200)



@require_GET
def descrizione_film(request, titolo_film):

    return render(request,template_name="streamify/descr_film.html", context={
        "film": Film.objects.get(titolo=titolo_film)
    }, status=200)




@require_GET
@login_required
def set_preferito(request, titolo_film, scelta):
    # Scelta può valere {yes, no}
    # yes --> verrà inserito tra i preferiti
    # no --> verrà rimosso dai preferiti

    logged_user = request.user

    if scelta == "yes":
        logged_user.film_preferiti.add(Film.objects.get(titolo=titolo_film))
    else:
        logged_user.film_preferiti.remove(Film.objects.get(titolo=titolo_film))

    return render(request, template_name="account.html", context={
        "logged_user": logged_user,
        "generi_dict": json.dumps(calcola_generi(request.user)),
        "recommended_films": calcola_recommendation_system(request.user)
    }, status=200)