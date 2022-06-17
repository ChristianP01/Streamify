from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import IntegerField
from django.contrib.postgres.fields import ArrayField
from django.db.models import Avg

CURRENT_YEAR = int(datetime.datetime.now().year)

DEFAULT_GENERIC_VALUE = "/" #Valore di default assegnato ai field che richiedono un default, non meglio specificato.


class Genere(models.Model):
    name=models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Generi"


class Film(models.Model):
    titolo = models.CharField(max_length=70)
    generi = models.ManyToManyField(Genere)
    anno_uscita = models.IntegerField(validators=[MinValueValidator(1888), MaxValueValidator(CURRENT_YEAR)])
    trama = models.TextField(max_length=800, null=True)

    #  {{ film.get_mediavoto }} per chiamarlo nell'HTML (NO PARENTESI) 
    def get_mediavoto(self):
        media_voto = Recensione.objects.filter(film=self).aggregate(Avg('voto'))["voto__avg"]
        
        if media_voto:
            return float(media_voto)
        else:
            return 1.0

    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name_plural = "Film"


# Modello rappresentante la classe Utente, i suoi fields sono le credenziali di accesso/registrazione.
class Utente(models.Model):
    username = models.CharField(max_length=25, primary_key=True)
    email = models.EmailField(max_length=50, default=DEFAULT_GENERIC_VALUE)
    password = models.CharField(max_length=25, default=DEFAULT_GENERIC_VALUE)
    nome = models.CharField(max_length=50, default=DEFAULT_GENERIC_VALUE)
    cognome = models.CharField(max_length=50, default=DEFAULT_GENERIC_VALUE)
    film_guardati = models.ManyToManyField(Film, default=None)
    
    def __str__(self):
        out = "Utente " + self.username + ", avente la e-mail " + self.email + ". La sua password è " + self.password + "."
        return out

    class Meta:
        verbose_name_plural = "Utenti"


class Recensione(models.Model):
    voto = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, default=DEFAULT_GENERIC_VALUE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, default=DEFAULT_GENERIC_VALUE)
    commento_scritto = models.CharField(max_length=500, default=None)

    def __str__(self):
        return f"Voto {self.voto} per {self.film}"

    class Meta:
        verbose_name_plural = "Recensioni"

        constraints = [
            models.UniqueConstraint(
                fields=['utente', 'film'],
                name='unique_constraint_utente_film'
            )
        ]