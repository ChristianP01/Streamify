from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Avg

CURRENT_YEAR = int(datetime.datetime.now().year)

DEFAULT_GENERIC_VALUE = "/" #Valore di default assegnato ai field che richiedono un default, non meglio specificato.


class Genere(models.Model):
    name=models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Generi"


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, password, email="email", **extra_fields ):
        user=self._create_user(email, password, True, True, **extra_fields)
        return user


class Film(models.Model):
    titolo = models.CharField(max_length=70)
    generi = models.ManyToManyField(Genere)
    anno_uscita = models.IntegerField(validators=[MinValueValidator(1888), MaxValueValidator(CURRENT_YEAR)])
    trama = models.TextField(max_length=800, null=True)

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
class Utente(AbstractBaseUser):
    username = models.CharField(max_length=25, primary_key=True)
    email = models.EmailField(max_length=50, default=DEFAULT_GENERIC_VALUE, unique=True)
    password = models.CharField(max_length=200, default=DEFAULT_GENERIC_VALUE)
    nome = models.CharField(max_length=50, default=DEFAULT_GENERIC_VALUE)
    cognome = models.CharField(max_length=50, default=DEFAULT_GENERIC_VALUE)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [ 'password', 'nome', 'cognome' ]

    objects = UserManager()
    
    # Related name sono nomi che indicano il nome con cui, in altri models, si dovrà accedere a questi parametri.
    film_guardati = models.ManyToManyField(Film, default=None, related_name="film_guardati")
    film_preferiti = models.ManyToManyField(Film, default=None, related_name="film_preferiti")

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def __str__(self):
        out = "Utente " + self.username + ", avente e-mail " + self.email + "."
        return out

    class Meta:
        verbose_name_plural = "Utenti"


class Recensione(models.Model):
    voto = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, default=DEFAULT_GENERIC_VALUE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, default=DEFAULT_GENERIC_VALUE)
    commento_scritto = models.CharField(max_length=500, default=None)

    def __str__(self):
        return f"{self.utente.username}: Voto {self.voto} per {self.film.titolo.replace('_', ' ')}"

    class Meta:
        verbose_name_plural = "Recensioni"

        constraints = [
            models.UniqueConstraint(
                fields=['utente', 'film'],
                name='unique_constraint_utente_film'
            )
        ]