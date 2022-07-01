from streamify.models import Film, Genere, Recensione, Utente
from django.test import TestCase

class TestModelFilm(TestCase):

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

        Recensione.objects.create(
            voto = 4,
            utente = self.test_user,
            film = self.test_film,
            commento_scritto = "..."
        )

    def test_model_film(self):
        self.assertEqual(self.test_film.get_mediavoto(), 4)
        self.assertEqual(self.test_film.__str__(), 'Spiderman')
