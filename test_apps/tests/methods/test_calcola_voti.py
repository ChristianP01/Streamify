from streamify.methods import calcola_generi, calcola_voti
from streamify.models import Film, Genere, Utente
from django.test import TestCase

class TestCalcolaVotiFilmNonRecensito(TestCase):

    def setUp(self):


        test_genere = Genere.objects.create(
            name="Azione"
        )

        self.test_film = Film.objects.create(
            titolo = 'Spiderman',
            anno_uscita = '2002',
            trama = 'Trama...'
        )
        self.test_film.generi.set((test_genere,))
        
        self.test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test')
        self.test_user.film_guardati.add(self.test_film, )
        
        self.test_user.set_password('testUser')
        self.test_user.save()

    def test_calcola_voti_film_non_recensito(self):
        self.assertEqual(calcola_voti(self.test_user, calcola_generi(self.test_user)), { 'Azione': 0 })