from urllib import request
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from my_auth.views import logged
from streamify.models import Utente
from streamify.templatetags.replace_titles import replace_titles

class TestLoginSuccess(TestCase):

    def setUp(self):
        self.example_title = "Titolo_del_film"
        
    def test_login_success(self):
        self.assertEqual(replace_titles(self.example_title), "Titolo del film")