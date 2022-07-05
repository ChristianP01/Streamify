from django.test import Client, TestCase
from streamify.models import Film, Genere, Utente

class TestSortFilmUp(TestCase):

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
        self.client.login(username='testUser', password='testUser')

        self.response = self.client.get('/streamify/catalogo_sort/up/')

    def test_sort_film_up(self):
        self.assertEqual(self.response.status_code, 200)

class TestSortFilmDown(TestCase):

    def setUp(self):

        example_genere = Genere.objects.create()

        test_film = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film.generi.set((example_genere,))

        self.client = Client()
        session = self.client.session
        session.save()

        self.response = self.client.get('/streamify/catalogo_sort/down/')

    def test_sort_film_down(self):
        self.assertEqual(self.response.status_code, 200)