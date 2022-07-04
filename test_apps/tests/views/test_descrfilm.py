from django.test import Client, TestCase
from streamify.models import Utente, Genere, Film

class TestDescrFilmLogged(TestCase):

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

        self.response = self.client.get('/streamify/descr_film/Spiderman/')

    def test_descr_film_logged(self):
        self.assertEqual(self.response.status_code, 200)


class TestDescrFilmAnonymous(TestCase):

    def setUp(self):

        example_genere = Genere.objects.create()

        test_film = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film.generi.set((example_genere,))

        self.client = Client()

        self.response = self.client.get('/streamify/descr_film/Spiderman/')

    def test_descr_film_anonymous(self):
        self.assertEqual(self.response.status_code, 200)