from django.test import Client, TestCase
from streamify.models import Film, Genere, Utente


class TestReviewSuccess(TestCase):

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

        self.response = self.client.post('/streamify/review/Spiderman/')

    def test_review_success(self):
        self.assertEqual(self.response.status_code, 200)


class TestReviewFail(TestCase):

    def setUp(self):
        
        self.client = Client()
        session = self.client.session
        session['logged_user'] = None
        session.save()

        self.response = self.client.post('/streamify/review/Spiderman/')

    def test_review_fail(self):
        self.assertEqual(self.response.status_code, 401)