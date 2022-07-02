from django.test import Client, TestCase
from streamify.models import Film, Genere, Utente


class TestMyReviewsLogged(TestCase):

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
            
        test_user.film_guardati.add(test_film)

        self.client = Client()
        self.client.login(username='testUser', password='testUser')

        self.response = self.client.post('/streamify/my_reviews/')

    def test_myreviews_logged(self):
        self.assertEqual(self.response.status_code, 200)