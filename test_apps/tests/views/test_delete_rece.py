from django.test import Client, TestCase
from streamify.models import Genere, Recensione, Utente, Film

class TestRemoveRecensione(TestCase):

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

        Recensione.objects.create(
            film=test_film,
            utente=test_user,
            voto=4,
            commento_scritto='...'
        )

        test_user.set_password('testUser')
        test_user.save()

        self.client = Client()
        self.client.login(username='testUser', password='testUser')

        self.response = self.client.get('/streamify/remove_rece/?titolo_film=Spiderman')
        
    def test_remove_recensione(self):
        self.assertEqual(self.response.status_code, 200)