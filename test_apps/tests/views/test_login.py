from django.test import Client, TestCase
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
            'username': 'testUser',
            'password': 'testUser'}

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
            'username': 'wrongUser',
            'password': 'wrongPwd'}

        self.client = Client()
        self.response = self.client.post('/auth/accedi/', creds)
        
    def test_login_fail(self):
        self.assertEqual(self.response.status_code, 401)