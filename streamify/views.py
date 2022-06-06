import json
from django.shortcuts import render
from django.views.generic import ListView
from streamify.methods import calcolaGeneri, calcolaPercents, calcolaVoti
from streamify.models import Film, Recensione, Utente, Genere
from django.contrib import messages
from django.db.models import Avg

# Contiene la dimensione del dizionario dei generi da considerare come preferiti, su cui applicare il RS.
RECOM_SYS_NUMS = 2

#---------------Carimento recensioni-------------------#
avgs = {}
# Dizionario contenente la coppia {titolo_film: voto}
for film in Film.objects.all():
    avgs[film.titolo] = Recensione.objects.filter(film=film).aggregate(Avg('voto'))
#-------------------------------------------------------------#

def homepage(request):

    # Resetto request.session in modo da simulare un logout completo.
    request.session.clear()

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
            "avgs": avgs
        })

    except:
        messages.error(request, "Credenziali errate!")
        return render(request,template_name="streamify/home.html")

def catalogo(request):
    # Qui ci entrerà un utente guest oppure dopo aver cliccato "Reset" nel catalogo.

    try:
        logged_user = request.session["logged_user"]
    except:
        logged_user = None

    return render(request,template_name="streamify/catalogo.html", context={
            "logged_user": logged_user,
            "film_list": Film.objects.all(),
            "avgs": avgs
        })

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
                "avgs": avgs
            })

        # Se invece l'ha già guardato
        else:
            messages.success(request, f"Hai già guardato {titolo_film}!")
            return render(request,template_name="streamify/catalogo.html", context={
                "film_list": Film.objects.all(),
                "logged_user": logged_user,
                "avgs": avgs
            })

    except:
        messages.error(request, "Effettua il login per guardare il film!")
        return render(request, template_name="home.html")

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

        print("Stampa informazioni riguardanti il recommendation system...")
        
        # Dizionario contenente i due generi meglio votati dall'utente
        logged_two_highest = sorted(calcolaVoti(utente, generi).items(), key=lambda x: x[1], reverse=True)\
                                                                                                                    [0:RECOM_SYS_NUMS]

        for other_user in Utente.objects.all():
            other_two_highest = sorted(calcolaVoti(other_user, calcolaGeneri(other_user)).items(),
                                                                    key=lambda x: x[1],
                                                                    reverse=True)[0:RECOM_SYS_NUMS]

            for i in range(RECOM_SYS_NUMS):
                if logged_two_highest[i][0] == other_two_highest[i][0]:
                    similarity = (100-100*( abs(logged_two_highest[i][1]-other_two_highest[i][1]) /5))
                    if similarity >= 90:
                        print(f"Genere {logged_two_highest[i][0]} con similanza del {similarity}%")


        #-------------------------------------------------------------------#

        return render(request, template_name="streamify/account.html", context={
            "logged_user": request.session["logged_user"],
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


def cercaFilm(request):

    # Non c'è bisogno di controllare l'utente loggato perchè chiunque dovrebbe poter cercare nel catalogo.
    # Quello che faccio qui è assegnargli un valore di default da ritornare al render
    try:
        logged_user = request.session["logged_user"]
    except:
        logged_user = None

    user_input = request.POST["film_search"]
    

    film_query = Film.objects.filter(titolo__startswith=user_input)

    return render(request,template_name="streamify/catalogo.html", context={
        "logged_user": logged_user,
        "film_list": film_query,
        "avgs": avgs
    })