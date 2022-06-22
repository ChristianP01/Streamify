from urllib import request
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from my_auth.views import logged
from streamify.models import Utente

class TestRegisterSuccess(TestCase):

    def setUp(self):

        creds = {
            'uname' :'testUser',
            'psw' : 'testUser',
            'email' : 'test@test.it',
            'nome' : 'Test',
            'cognome' : 'test'}

        self.client = Client()
        self.response = self.client.post('/auth/registrati/', creds)
        
    def test_register_success(self):
        self.assertEqual(self.response.status_code, 200)



class TestRegisterFail(TestCase):

    def setUp(self):

        test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test')

        creds = {
            'uname' :'testUser',
            'psw' : 'testUser',
            'email' : 'test@test.it',
            'nome' : 'Test',
            'cognome' : 'test'}

        self.client = Client()
        self.response = self.client.post('/auth/registrati/', creds)
        
    def test_register_fail(self):
        self.assertEqual(self.response.status_code, 409)
