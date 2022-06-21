from urllib import request
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from my_auth.views import logged
from streamify.models import Utente

class TestNewUser(TestCase):

    def setUp(self):
        """Testa il corretto login di un utente (esistente)"""
        c = Client()
        response = c.post('/auth/accedi/', {'uname': 'ChristianP01', 'psw': 'gg'})
        print(response)
    
    def test_creaUser(self):
        self.assertEqual(Utente.objects.count(), 1)