from audioop import avg
import json
from django.shortcuts import render
from django.views.generic import ListView
from numpy import append
from streamify.methods import calcolaGeneri, calcolaPercents, calcolaVoti
from streamify.models import Film, Recensione, Utente, Genere
from django.contrib import messages
from django.db.models import Avg
from django.views.decorators.http import require_http_methods

# Contiene la dimensione del dizionario dei generi da considerare come preferiti, su cui applicare il RS.
RECOM_SYS_NUMS = 2

#---------------Carimento recensioni-------------------#
avgs = {}
# Dizionario contenente la coppia {titolo_film: voto}
for film in Film.objects.all():
    voto_medio = Recensione.objects.filter(film=film).aggregate(Avg('voto'))["voto__avg"]

    if voto_medio is not None:
        avgs[film.titolo] = float(voto_medio)
    else:
        avgs[film.titolo] = 1.0
#-------------------------------------------------------------#

#---------------------Lista generi-------------------------#
# Serve al catalogo per rimanere aggiornato sui nuovi generi (lato HTML)
lista_generi = Genere.objects.all()
#-------------------------------------------------------------#

@require_http_methods("GET")
def homepage(request):

    # Resetto request.session in modo da simulare un logout completo.
    request.session.clear()

    return render(request,template_name="streamify/home.html")

@require_http_methods("POST")
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

@require_http_methods("POST")
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
            "avgs": avgs,
            "lista_generi": lista_generi
        })

    except:
        messages.error(request, "Credenziali errate!")
        return render(request,template_name="streamify/home.html")

@require_http_methods(["GET","POST"])
def catalogo(request):
    # Qui ci entrerà un utente guest oppure dopo aver cliccato "Reset" nel catalogo.

    try:
        logged_user = request.session["logged_user"]
    except:
        logged_user = None

    return render(request,template_name="streamify/catalogo.html", context={
            "logged_user": logged_user,
            "film_list": Film.objects.all(),
            "avgs": avgs,
            "lista_generi": lista_generi
        })

@require_http_methods(["GET","POST"])
def guardaFilm(request, titolo_film):

    #Se un utente prova a guardare un film senza essere loggato (ad esempio scrivendo direttamente l'URL del film
    # oppure i cookie della sessione scadono, ritorno None come utente per avvisare l'utente di effettuare il login.)
    try:
        logged_user = request.session["logged_user"]

        if Film.objects.filter(titolo=titolo_film)[0] not in Utente.objects.filter(username=logged_user)[0].film_guardati.all():

            #Update del DB se l'utente non ha ancora guardato il film
            Utente.objects.filter(username=logged_user)[0].film_guardati.add(Film.objects.filter(titolo=titolo_film)[0])

            messages.success(request, f"{titolo_film} guardato con successo!")
            return render(request,template_name="streamify/catalogo.html", context={
                "film_list": Film.objects.all(),
                "logged_user": logged_user,
                "avgs": avgs,
                "lista_generi": lista_generi
            })

        # Se invece l'ha già guardato
        else:
            messages.success(request, f"Hai già guardato {titolo_film}!")
            return render(request,template_name="streamify/catalogo.html", context={
                "film_list": Film.objects.all(),
                "logged_user": logged_user,
                "avgs": avgs,
                "lista_generi": lista_generi
            })

    except:
        messages.error(request, "Effettua il login per guardare il film!")
        return render(request, template_name="home.html")

@require_http_methods(["GET", "POST"])
def account(request):

    # Non posso fare entrare un utente in questa pagina se non è loggato, quindi ritorno None.
    try:

        # Se l'utente è entrato correttamente, lo cerco nel database al fine di ottenere i film che ha guardato.
        utente = Utente.objects.filter(username=request.session["logged_user"])[0]

        generi = calcolaGeneri(utente)

        # Mi salvo un riferimento alla lista dei generi, in modo da poterla ricaricare in futuro (review)
        request.session["generi"] = generi

        #---------------- Recommendation System ------------------#
        
        # Comparo il percents dell'utente loggato con quello di tutti gli altri utenti
        # Funziona così: creo un dizionario col formato {genere: % sul totale}.
        # Dopo prendo i 2/3 valori più alti del dizionario (rappresenteranno i generi preferiti)
        # e faccio il reciproco della differenza con ogni utente (1-differenza).
        # Questo mi permetterà di trovare possibili utenti con gusti simili.
        # Per ogni coppia (this_user, other_user) guardo solo se la differenza è >90, per avere buone corrispondenze
        # Se >90, passo a guardare i voti medi a quel genere e se il reciproco della differenza è >90
        # Consiglio i film in più relativi a quel genere guardati da quell'utente.
        # P.S. Da utente voglio ricevere consigli solo sui miei generi preferiti.

        # Nuova logica: Creo un dizionario col formato {genere: voto_medio}, prendo i due valori più alti. 
        # Essi rappresenteranno i generi preferiti, confronterò quelli dell'utente corrente con quelli di ogni altro utente.
        # Se ci sarà corrispondenza sul nome del genere (ovvero un gusto in comune), controllo se il voto ha un valore
        # di similanza >90. Se è così, consiglio i film che quell'utente avrà guardato in più.
        recommended_films = []

        # Dizionario contenente i due generi meglio votati dall'utente
        logged_two_highest = sorted(calcolaVoti(utente, generi).items(), key=lambda x: x[1], reverse=True)\
                                                                                                                    [0:RECOM_SYS_NUMS]

        if len(logged_two_highest) < RECOM_SYS_NUMS:
            return render(request, template_name="streamify/account.html", context={
            "logged_user": request.session["logged_user"],
            "lista_film": utente.film_guardati.all(),
            "recommended_films": None
            })


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

                            # Lista di tutti i film guardati da other_user ma non da logged_user
                            
                            for film in other_user.film_guardati.all():
                                if film not in utente.film_guardati.all() and \
                                     Genere.objects.filter(name=logged_genre[0])[0] in film.generi.all():
                                        recommended_films.append(film)


        #-------------------------------------------------------------------#


        return render(request, template_name="streamify/account.html", context={
            "logged_user": request.session["logged_user"],
            "lista_film": utente.film_guardati.all(),
            "generi_dict": json.dumps(generi),
            "recommended_films": recommended_films
        })

    except:
        return render(request, template_name="streamify/account.html", context={
        "logged_user": None,
        "lista_film": None,
        "recommended_films": None
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

        try:
            if Recensione.objects.get(utente=user, film=film):
                messages.error(request, "Hai già recensito questo film!")
                return render(request, template_name="account.html", context={
                    "logged_user": user,
                    "lista_film": user.film_guardati.all(),
                    "generi_dict": json.dumps(request.session["generi"])
                })
        
        except:
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

@require_http_methods(["POST"])
def cercaFilm(request):

    # Non c'è bisogno di controllare l'utente loggato perchè chiunque dovrebbe poter cercare nel catalogo.
    # Quello che faccio qui è assegnargli un valore di default da ritornare al render
    try:
        logged_user = request.session["logged_user"]
    except:
        logged_user = None

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


    film_query = Film.objects.filter(titolo__startswith=user_input, generi__name=genre_input)
    
    film_query_matched = []
    for film in film_query:
        if film.titolo in avgs.keys():
            if avgs[film.titolo] >= min_score and avgs[film.titolo] <= max_score:
                film_query_matched.append(film)
                
    return render(request,template_name="streamify/catalogo.html", context={
        "logged_user": logged_user,
        "film_list": film_query_matched,
        "avgs": avgs,
        "lista_generi": lista_generi
    })