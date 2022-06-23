from urllib import request
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from my_auth.views import logged
from streamify.models import Utente

class TestHomepage(TestCase):

    def setUp(self):

        self.client = Client()
        self.response = self.client.get('/streamify/home/')
        
    def test_homepage(self):
        self.assertEqual(self.response.status_code, 200)