from django.test import Client, TestCase
from streamify.models import Genere, Utente, Film

class TestChatSuccess(TestCase):

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
        test_user.film_guardati.add(test_film)

        self.client = Client()
        session = self.client.session
        session["logged_user"] = test_user.username
        session.save()

        self.response = self.client.get('/chatify/chat/Spiderman/')
        
    def test_chat_success(self):
        self.assertEqual(self.response.status_code, 200)


class TestChatAnonymous(TestCase):

    def setUp(self):

        example_genere = Genere.objects.create()

        test_film = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film.generi.set((example_genere,))

        self.client = Client()
        self.response = self.client.get('/chatify/chat/Spiderman/')
        
    def test_chat_success(self):
        self.assertEqual(self.response.status_code, 401)


class TestChatFilmNotWatched(TestCase):

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
        session["logged_user"] = test_user.username
        session.save()

        self.client = Client()
        self.response = self.client.get('/chatify/chat/Spiderman/')
        
    def test_chat_film_not_watched(self):
        self.assertEqual(self.response.status_code, 401)