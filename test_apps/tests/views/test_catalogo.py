from urllib import request
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from my_auth.views import logged
from streamify.models import Utente


class TestCatalogoSuccess(TestCase):

    def setUp(self):

        test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test')
        
        creds = {
            'uname': 'testUser',
            'psw': 'testUser'}

        self.client = Client()
        self.response = self.client.post('/streamify/catalogo/', creds)

    def test_catalogo_success(self):
        self.assertEqual(self.response.status_code, 200)