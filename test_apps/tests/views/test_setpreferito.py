from django.test import Client, TestCase
from streamify.models import Film, Genere, Utente

class TestSetPreferitoYesLogged(TestCase):

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
        session['logged_user'] = test_user.username
        session['generi'] = '...'
        session['recommended_films'] = '...'
        session.save()

        self.response = self.client.get('/streamify/set_preferito/Spiderman/yes/')

    def test_set_preferito_yes_logged(self):
        self.assertEqual(self.response.status_code, 200)


class TestSetPreferitoNoLogged(TestCase):

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
        session['logged_user'] = test_user.username
        session['generi'] = '...'
        session['recommended_films'] = '...'
        session.save()

        self.response = self.client.get('/streamify/set_preferito/Spiderman/no/')

    def test_set_preferito_no_logged(self):
        self.assertEqual(self.response.status_code, 200)



class TestSetPreferitoYesAnonymous(TestCase):

    def setUp(self):

        example_genere = Genere.objects.create()

        test_film = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film.generi.set((example_genere,))
        
        self.client = Client()
        session = self.client.session
        session['generi'] = '...'
        session['recommended_films'] = '...'
        self.response = self.client.get('/streamify/set_preferito/Spiderman/yes/')

    def test_set_preferito_yes_anonymous(self):
        self.assertEqual(self.response.status_code, 401)


class TestSetPreferitoNoAnonymous(TestCase):

    def setUp(self):

        example_genere = Genere.objects.create()

        test_film = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film.generi.set((example_genere,))
        
        self.client = Client()
        session = self.client.session
        session['generi'] = '...'
        session['recommended_films'] = '...'
        self.response = self.client.get('/streamify/set_preferito/Spiderman/no/')

    def test_set_preferito_no_anonymous(self):
        self.assertEqual(self.response.status_code, 401)