from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import IntegerField
from django.contrib.postgres.fields import ArrayField

CURRENT_YEAR = int(datetime.datetime.now().year)



class Genere(models.Model):
    name=models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Generi"


class Film(models.Model):
    id = models.AutoField(primary_key=True)
    titolo = models.CharField(max_length=70)
    generi = models.ManyToManyField(Genere)
    anno_uscita = models.IntegerField(validators=[MinValueValidator(1888), MaxValueValidator(CURRENT_YEAR)])
    valutazione = models.IntegerField(default=None)

    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name_plural = "Film"


class Recensione(models.Model):
    voto = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return f"Voto {self.voto} per {self.film}"

    class Meta:
        verbose_name_plural = "Recensioni"


# Modello rappresentante la classe Utente, i suoi fields sono le credenziali di accesso/registrazione.
class Utente(models.Model):
    username = models.CharField(max_length=25, primary_key=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    film_guardati = models.ManyToManyField(Film, default=None)
    recensioni = models.ManyToManyField(Recensione, default=None) 
    
    def __str__(self):
        out = "Utente " + self.username + ", avente la e-mail " + self.email + ". La sua password è " + self.password + "."
        return out

    class Meta:
        verbose_name_plural = "Utenti"