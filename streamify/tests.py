from urllib import request, response
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from my_auth.views import logged
from streamify.models import Utente

class TestRegistrati(TestCase):

    def setUp(self):
        """Testa la corretta registrazione di un utente (esistente)"""
        c = Client()
        self.response = c.post('/auth/registrati/', {
            'uname': 'testUser',
            'psw': 'test',
            'email': 'test@test.it',
            'nome': 'Test',
            'cognome': 'test'})
    
    def test_registraUser(self):
        self.assertEqual(self.response.status_code, 200)

class TestLogin(TestCase):

    def setUp(self):
        """Testa il corretto login di un utente (esistente)"""
        c = Client()
        self.response = c.post('/auth/accedi/', {'uname': 'ChristianP01', 'psw': 'gg'})
    
    def test_loginUser(self):
        self.assertEqual(self.response.status_code, 200)