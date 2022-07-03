from streamify.models import Film, Genere, Recensione, Utente
from django.test import TestCase

class TestModelRecensione(TestCase):

    def setUp(self):

        self.test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test')

        self.test_film = Film.objects.create(
            titolo = 'Spiderman',
            anno_uscita = '2002',
            trama = 'Trama...'
        )
        self.test_film.generi.set((Genere.objects.create(),))

        self.test_rece = Recensione.objects.create(
            voto = 4,
            utente = self.test_user,
            film = self.test_film,
            commento_scritto = "..."
        )

    def test_model_recensione(self):
        self.assertEqual(self.test_rece.__str__(), "testUser: Voto 4 per Spiderman")