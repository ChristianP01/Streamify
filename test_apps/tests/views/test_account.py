from urllib import request
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from my_auth.views import logged
from streamify.models import Utente


class TestAccountSuccess(TestCase):

    def setUp(self):

        test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test')
        
        self.client = Client()
        session = self.client.session
        session['logged_user'] = test_user.username
        session.save()

        self.response = self.client.post('/streamify/account/')

    def test_account_success(self):
        self.assertEqual(self.response.status_code, 200)


class TestAccountFail(TestCase):

    def setUp(self):

        self.client = Client()
        self.client.session['logged_user'] = None
        self.client.session.save()

        self.response = self.client.post('/streamify/account/')

    def test_account_fail(self):
        self.assertEqual(self.response.status_code, 401)