"""
Questo file dovrebbe fungere da interfaccia stile Java, l'idea è quella di separare la logica relativa a Django
da quella che mi serve in Python puro.
"""

from .models import Genere, Recensione, Utente

# Creo il dizionario con la sintassi {genere: numero_di_film_guardati_di_quel_genere}
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
    RECOM_SYS_NUMS = 2

    recommended_films = {}

    generi = calcola_generi(utente)
    logged_two_highest = sorted(calcola_voti(utente, generi).items(), key=lambda x: x[1], reverse=True)\
                                                                                                                [0:RECOM_SYS_NUMS]

    if len(logged_two_highest) < RECOM_SYS_NUMS:
        return {}

    # Struttura logged_genre/other_genre --> ['nome_genere': 'voto_genere']
    for other_user in Utente.objects.all().exclude(username=utente.username):
        
        other_two_highest = sorted(calcola_voti(other_user, calcola_generi(other_user)).items(),
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
                                    recommended_films[film.titolo] = int(similarity)

    return recommended_films