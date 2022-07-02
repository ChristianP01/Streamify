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

        test_user.set_password('testUser')
        test_user.save()

        self.client = Client()
        self.client.login(username='testUser', password='testUser')

        self.response = self.client.get('/chatify/chat/Spiderman/')
        
    def test_chat_success(self):
        self.assertEqual(self.response.status_code, 200)


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

        test_user.set_password('testUser')
        test_user.save()

        self.client = Client()
        self.client.login(username='testUser', password='testUser')
        
        self.response = self.client.get('/chatify/chat/Spiderman/')
        
    def test_chat_film_not_watched(self):
        self.assertEqual(self.response.status_code, 401)