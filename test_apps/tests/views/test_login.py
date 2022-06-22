from urllib import request
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from my_auth.views import logged
from streamify.models import Utente


class TestLoginSuccess(TestCase):

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
        self.response = self.client.post('/auth/accedi/', creds)
        
    def test_login_success(self):
        self.assertEqual(self.response.status_code, 200)




class TestLoginFail(TestCase):

    def setUp(self):

        test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test')
        
        creds = {
            'uname': 'wrongUser',
            'psw': 'wrongPwd'}

        self.client = Client()
        self.response = self.client.post('/auth/accedi/', creds)
        
    def test_login_fail(self):
        self.assertEqual(self.response.status_code, 401)