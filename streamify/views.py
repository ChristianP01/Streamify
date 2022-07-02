import json
from django.shortcuts import render
from streamify.methods import calcolaGeneri, calcolaVoti
from streamify.models import Film, Recensione, Utente, Genere
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Contiene la dimensione del dizionario dei generi da considerare come preferiti, su cui applicare il RS.
RECOM_SYS_NUMS = 3

@require_http_methods("GET")
def homepage(request):

    # Resetto request.session in modo da simulare un logout completo.
    request.session.clear()

    return render(request,template_name="streamify/home.html")


@require_http_methods(["GET","POST"])
def catalogo(request):
    # Qui ci entrerà un utente guest oppure dopo aver cliccato "Reset" nei filtri del catalogo

    logged_user = request.user

    return render(request,template_name="streamify/catalogo.html", context={
            "logged_user": logged_user,
            "film_list": Film.objects.all(),
            "lista_generi": Genere.objects.all()
        }, status=200)

@require_http_methods(["GET","POST"])
@login_required
def guardaFilm(request, titolo_film):

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


@require_http_methods(["GET", "POST"])
@login_required
def account(request):

    utente = request.user
    
    generi = calcolaGeneri(utente)

    # Le salvo nel dizionario di sessione, siccome sarà usata in altre views
    request.session["generi"] = generi

    # Lista contenente i film suggeriti dal recommendation system
    recommended_films = []


    # Dizionario contenente i due generi meglio votati dall'utente
    logged_two_highest = sorted(calcolaVoti(utente, generi).items(), key=lambda x: x[1], reverse=True)\
                                                                                                                [0:RECOM_SYS_NUMS]
    
    if len(logged_two_highest) < RECOM_SYS_NUMS:
        return render(request, template_name="streamify/account.html", context={
        "logged_user": utente,
        "generi_dict": json.dumps(generi),
        "recommended_films": None
        }, status=206)


    for other_user in Utente.objects.all().exclude(username=utente.username):
        
        other_two_highest = sorted(calcolaVoti(other_user, calcolaGeneri(other_user)).items(),
                                                                key=lambda x: x[1],
                                                                reverse=True)[0:RECOM_SYS_NUMS]

        for logged_genre in logged_two_highest:
            for other_genre in other_two_highest:

                if logged_genre[0] == other_genre[0]:
                    similarity = (100-100*( abs(logged_genre[1]-other_genre[1]) /5))
                    if similarity >= 80:

                        # Ritorno i film guardati "in più" da other_user --> logged_user
                        for film in other_user.film_guardati.all():
                            if film not in utente.film_guardati.all() and \
                                    Genere.objects.get(name=logged_genre[0]) in film.generi.all():
                                    recommended_films.append(film.titolo)

    # Salvo i film nella sessione al fine di poterli ritornare in futuro.
    request.session["recommended_films"] = recommended_films

    # Rimuoviamo i doppioni (dato che potrebbero essere suggeriti da più utenti).
    recommended_films = list(set(recommended_films))

    #-------------------------------------------------------------------#

    return render(request, template_name="streamify/account.html", context={
        "logged_user": utente,
        "generi_dict": json.dumps(generi),
        "recommended_films": recommended_films
    }, status=200)
    

@require_http_methods(["GET", "POST"])
@login_required
def review(request, titolo_film):

    logged_user = request.user
    film = Film.objects.get(titolo=titolo_film)
    request.session["film"] = film.titolo

    return render(request, template_name="review.html", context={
        "logged_user": logged_user,
        "film": film,
        "lista_recensioni": Recensione.objects.filter(film=film)
    }, status=200)
        

@login_required
def review_final(request):

    value = request.POST["selected_star"]
    commento_scritto = request.POST["commento_scritto"]

    film = Film.objects.get(titolo=request.session["film"])
    logged_user = request.user

    if len(Recensione.objects.filter(utente=logged_user, film=film)) == 0:
        new_rece = Recensione(voto=value, utente=logged_user, film=film, commento_scritto=commento_scritto)
        new_rece.save()

        messages.add_message(request, messages.SUCCESS, "Hai recensito correttamente il film!")
        return render(request, template_name="account.html", context={
            "logged_user": logged_user,
            "generi_dict": json.dumps(request.session["generi"]),
            "recommended_films": request.session["recommended_films"]
        }, status=200)


    else:
        messages.add_message(request, messages.WARNING, "Hai già recensito questo film!")
        return render(request, template_name="account.html", context={
            "logged_user": logged_user,
            "generi_dict": json.dumps(request.session["generi"]),
            "recommended_films": request.session["recommended_films"]
        }, status=409)


@require_http_methods(["POST"])
def cercaFilm(request):

    logged_user = request.user

    user_input = request.POST["film_search_title"]
    genre_input = request.POST["generi"]
    min_score = request.POST["min_score"]
    max_score = request.POST["max_score"]

    try:
        1 + float(min_score)
        min_score = float(min_score)
    except:
        min_score = 1.0

    try:
        1 + float(max_score)
        max_score = float(max_score)
    except:
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


@require_http_methods(["GET","POST"])
@login_required
def my_reviews(request):

    logged_user = request.user

    return render(request,template_name="streamify/user_reviews.html", context={
        "film_list": logged_user.film_guardati.all(),
        "lista_recensioni": Recensione.objects.filter(utente=logged_user)
    }, status=200)



@require_http_methods(["GET","POST"])
def film_sort(request, sort_type):
    # sort_type = {up | down} in base al tipo di sorting richiesto.

    if sort_type == "up":
        sort_type = True
    else:
        sort_type = False

    return render(request,template_name="streamify/catalogo.html", context={
        "film_list": sorted(Film.objects.all(), key= lambda film: film.get_mediavoto(), reverse=sort_type),
        "lista_generi": Genere.objects.all()
    }, status=200)

@require_http_methods(["GET","POST"])
def descrizione_film(request, titolo_film):

    return render(request,template_name="streamify/descr_film.html", context={
        "film": Film.objects.get(titolo=titolo_film)
    }, status=200)

@require_http_methods(["GET","POST"])
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
        "generi_dict": json.dumps(request.session["generi"]),
        "recommended_films": request.session["recommended_films"]
    }, status=200)