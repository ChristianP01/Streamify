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