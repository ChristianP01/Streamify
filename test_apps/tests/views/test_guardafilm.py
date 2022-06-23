from django.test import Client, TestCase
from streamify.models import Film, Genere, Utente

class TestGuardafilmSuccess(TestCase):

    def setUp(self):

        test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test')

        example_genere = Genere.objects.create()

        test_film = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film.generi.set((example_genere,))

        self.client = Client()
        session = self.client.session
        session['logged_user'] = test_user.username
        session.save()

        self.response = self.client.get('/streamify/guarda_film/Spiderman/')

    def test_guardafilmsuccess(self):
        self.assertEqual(self.response.status_code, 200)



class TestGuardafilmFail(TestCase):

    def setUp(self):

        example_genere = Genere.objects.create()

        test_film = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film.generi.set((example_genere,))
        
        self.client = Client()
        self.response = self.client.get('/streamify/guarda_film/Spiderman/')

    def test_guardafilm_fail(self):
        self.assertEqual(self.response.status_code, 401)


class TestGuardafilmGuardato(TestCase):

    def setUp(self):

        test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test')

        example_genere = Genere.objects.create()

        test_film = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film.generi.set((example_genere,))

        self.client = Client()
        session = self.client.session
        session['logged_user'] = test_user.username
        session.save()

        self.response = self.client.get('/streamify/guarda_film/Spiderman/')
        self.response = self.client.get('/streamify/guarda_film/Spiderman/')

    def test_guardafilm_guardato(self):
        self.assertEqual(self.response.status_code, 409)