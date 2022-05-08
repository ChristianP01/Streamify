from django.db import models

class Utente(models.Model):
    username = models.CharField(max_length=25, primary_key=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    
    def __str__(self):
        out = "Utente " + self.username + ", avente la e-mail " + self.email + ". La sua password è " + self.password + "."
        return out

    class Meta:
        verbose_name_plural = "Utenti"