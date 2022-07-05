from django.test import Client, TestCase
from streamify.models import Film, Genere, Utente

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

        test_user.set_password('testUser')
        test_user.save()

        self.client = Client()
        self.client.login(username='testUser', password='testUser')

        #---------------------------Ricerca 1------------------------------#

        data = {
            'film_search_title' : test_film.titolo,
            'generi' : '',
            'min_score' : 3,
            'max_score' : ''
        }
        self.response = self.client.post('/streamify/cercaFilm/', data)

        #---------------------------Ricerca 2------------------------------#

        data = {
            'film_search_title' : test_film.titolo,
            'generi' : '',
            'min_score' : '',
            'max_score' : ''
        }
        self.response = self.client.post('/streamify/cercaFilm/', data)

        #---------------------------Ricerca 3------------------------------#

        data = {
            'film_search_title' : test_film.titolo,
            'generi' : '',
            'min_score' : '',
            'max_score' : 3
        }
        self.response = self.client.post('/streamify/cercaFilm/', data)

        #---------------------------Ricerca 4------------------------------#

        data = {
            'film_search_title' : '',
            'generi' : '',
            'min_score' : 2,
            'max_score' : 4
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
        self.client.login(username='testUser', password='testUser')

        data = {
            'film_search_title' : test_film.titolo,
            'generi' : '',
            'min_score' : 3,
            'max_score' : ''
        }

        self.response = self.client.post('/streamify/cercaFilm/', data)

    def test_cercafilm_success(self):
        self.assertEqual(self.response.status_code, 200)
