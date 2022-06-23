from urllib import request
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from pyrsistent import v
from my_auth.views import logged
from streamify.models import Film, Genere, Recensione, Utente


class TestCercaFilmLogged(TestCase):

    def setUp(self):

        example_genere = Genere.objects.create()

        test_film = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film.generi.set((example_genere,))

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

        data = {
            'film_search_title' : test_film.titolo,
            'generi' : '',
            'min_score' : 3,
            'max_score' : ''
        }

        self.response = self.client.post('/streamify/cercaFilm/', data)

    def test_cercafilm_success(self):
        self.assertEqual(self.response.status_code, 200)


class TestCercaFilmAnonymous(TestCase):

    def setUp(self):

        example_genere = Genere.objects.create()

        test_film = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film.generi.set((example_genere,))

        self.client = Client()
        session = self.client.session
        session['logged_user'] = None
        session.save()

        data = {
            'film_search_title' : test_film.titolo,
            'generi' : '',
            'min_score' : 3,
            'max_score' : ''
        }

        self.response = self.client.post('/streamify/cercaFilm/', data)

    def test_cercafilm_success(self):
        self.assertEqual(self.response.status_code, 200)
