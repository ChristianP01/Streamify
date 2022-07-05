from django.test import Client, TestCase
from streamify.models import Genere, Recensione, Utente, Film

class TestUpdateDBSuccess(TestCase):

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

        self.response = self.client.get('/db_ops/update_db/?titolo_film=Spiderman&nuovo_voto=5&nuovo_commento=Bellissimo!')
        
    def test_update_db_success(self):
        self.assertEqual(self.response.status_code, 200)



class TestUpdateDBLower(TestCase):

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

        self.response = self.client.get('/db_ops/update_db/?titolo_film=Spiderman&nuovo_voto=-3&nuovo_commento=Orribile!')
        
    def test_update_db_lower(self):
        self.assertEqual(self.response.status_code, 200)



class TestUpdateDBUpper(TestCase):

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

        self.response = self.client.get('/db_ops/update_db/?titolo_film=Spiderman&nuovo_voto=9&nuovo_commento=Bellissimo!')
        
    def test_update_db_upper(self):
        self.assertEqual(self.response.status_code, 200)