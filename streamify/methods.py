"""
Questo file dovrebbe fungere da interfaccia stile Java, l'idea è quella di separare la logica relativa a Django
da quella che mi serve in Python puro.
"""

from .models import Genere, Recensione, Utente

# Creo il dizionario con la sintassi {'genere': numero_di_film_guardati_di_quel_genere}
# Questo mi serve per disegnare il grafico e gestire il recommendation system
def calcola_generi(utente):
    generi = {}

    for film in utente.film_guardati.all():
        for genere in film.generi.all():
            if genere.name not in generi:
                generi[genere.name] = 1
            else:
                generi[genere.name] += 1

    for genere in Genere.objects.all():
        if genere.name not in generi:
            generi[genere.name] = 0

    return generi


# Si occupa di creare il dizionario dei voti dell'utente a ogni genere, secondo la struttura {'genere': 'media_voto'}
def calcola_voti(utente, generi):
    voti = {}

    for film in utente.film_guardati.all():
        try:
            voto_recensione = int(Recensione.objects.get(utente=utente, film=film).voto)
        except Recensione.DoesNotExist:
            voto_recensione = 0

        # Somma dei voti delle recensioni
        for genere in film.generi.all():
            if genere.name not in voti:
                voti[genere.name] = voto_recensione
            else:
                voti[genere.name] += voto_recensione

    # Calcolo media vera e propria
    for genere in voti:
        voti[genere] = voti[genere] / generi[genere]

    return voti



def calcola_recommendation_system(utente):

    # Contiene la dimensione del dizionario dei generi da considerare come preferiti, su cui applicare il RS.
    RECOM_SYS_NUMS = 3

    recommended_films = {}

    logged_highest = sorted(calcola_voti(utente, calcola_generi(utente)).items(), key=lambda x: x[1], reverse=True)\
                                                                                                                [0:RECOM_SYS_NUMS]

    # Se la valutazione dell'ultimo elemento della lista (meno valutato tra i preferiti dell'utente) è = 0, vuol dire che l'utente
    # ha visto meno generi di quelli necessari per ottenere consigli dal recommendation system. Questo è garantito dal fatto
    # che la lista è ordinata.
    if len(logged_highest) < RECOM_SYS_NUMS or logged_highest[RECOM_SYS_NUMS-1][1] == 0:
        return {}

    # Struttura logged_genre/other_genre --> [('nome_genere', 'voto_genere'), (...)]
    for logged_genre in logged_highest:
        genre_cont = 0

        for other_user in Utente.objects.all().exclude(username=utente.username):
        
            other_highest = sorted(calcola_voti(other_user, calcola_generi(other_user)).items(),
                                                                    key=lambda x: x[1],
                                                                    reverse=True)[0:RECOM_SYS_NUMS]

            for other_genre in other_highest:

                if logged_genre[0] == other_genre[0]:
                    similarity = (100-100*( abs(logged_genre[1]-other_genre[1]) /5))
                    if similarity >= 80:

                        # Ritorno i film guardati "in più" da other_user --> logged_user
                        for film in other_user.film_guardati.all():
                            if film not in utente.film_guardati.all() and Genere.objects.get(name=logged_genre[0]) in film.generi.all():
                                genre_cont += 1

                                if film.titolo not in recommended_films:
                                    recommended_films[film.titolo] = int(similarity)
                                    
                                else:
                                    recommended_films[film.titolo] = ((recommended_films[film.titolo]*(genre_cont-1)) + int(similarity)) / genre_cont
                            

    return recommended_films