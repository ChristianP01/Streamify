from django.test import Client, TestCase
from streamify.models import Film, Genere, Utente


class TestReviewFinalSuccess(TestCase):

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
        session = self.client.session
        session['film'] = test_film.titolo
        session['generi'] = '...'
        session['recommended_films'] = '...'
        session.save()
        self.client.login(username='testUser', password='testUser')


        data = {
            'selected_star': 3,
            'commento_scritto': 'Commento...'
        }

        self.response = self.client.post('/streamify/review_final/', data)

    def test_review_final_success(self):
        self.assertEqual(self.response.status_code, 200)


class TestReviewFinalSenzaVoto(TestCase):

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
        session = self.client.session
        session['film'] = test_film.titolo
        session['generi'] = '...'
        session['recommended_films'] = '...'
        session.save()
        self.client.login(username='testUser', password='testUser')


        data = {
            'selected_star': '',
            'commento_scritto': 'Commento...'
        }

        self.response = self.client.post('/streamify/review_final/', data)

    def test_review_final_senza_voto(self):
        self.assertEqual(self.response.status_code, 206)


class TestReviewFinalGiaLasciata(TestCase):

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
        session = self.client.session
        session['film'] = 'Spiderman'
        session['generi'] = '...'
        session['recommended_films'] = '...'
        session.save()
        self.client.login(username='testUser', password='testUser')

        data = {
            'selected_star': 3,
            'commento_scritto': 'Commento...'
        }

        self.response = self.client.post('/streamify/review_final/', data)
        self.response = self.client.post('/streamify/review_final/', data)

    def test_review_gia_lasciata(self):
        self.assertEqual(self.response.status_code, 409)