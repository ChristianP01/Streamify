from urllib import request
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from pyrsistent import v
from my_auth.views import logged
from streamify.models import Film, Genere, Recensione, Utente


class TestAccountSuccess(TestCase):

    def setUp(self):

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

        self.response = self.client.post('/streamify/account/')

    def test_account_success(self):
        self.assertEqual(self.response.status_code, 204)


class TestAccountFail(TestCase):

    def setUp(self):

        self.client = Client()
        session = self.client.session
        session['logged_user'] = None
        session.save()

        self.response = self.client.post('/streamify/account/')

    def test_account_fail(self):
        self.assertEqual(self.response.status_code, 401)


class TestAccountRecommendedSystem(TestCase):

    def setUp(self):

        test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test')

        other_user = Utente.objects.create(
            username='otherUser',
            password='otherUser',
            email='othertest@test.it',
            nome='Other',
            cognome='test')

        #---------------Generazione generi---------------#
        gen1 = Genere.objects.create(name="Azione")
        gen2 = Genere.objects.create(name="Avventura")
        gen3 = Genere.objects.create(name="Horror")
        gen4 = Genere.objects.create(name="Romantico")
        gen5 = Genere.objects.create(name="Comico")
        #------------------------------------------------------#
        
        #--------------Generazione film------------------#
        test_film1 = Film.objects.create(
            titolo='Spiderman',
            anno_uscita='2022',
            trama='Trama...')
        test_film1.generi.set((gen1, gen2))

        test_film2 = Film.objects.create(
            titolo='Stranger Things',
            anno_uscita='2022',
            trama='Trama...')
        test_film2.generi.set((gen1, gen2))

        test_film3 = Film.objects.create(
            titolo='Attacco Dei Giganti',
            anno_uscita='2022',
            trama='Trama...')
        test_film3.generi.set((gen1, gen2))

        test_user.film_guardati.add(test_film1)
        test_user.film_guardati.add(test_film2)
        other_user.film_guardati.add(test_film1)
        other_user.film_guardati.add(test_film2)
        other_user.film_guardati.add(test_film3)
        #-------------------------------------------------------#

        #--------------Generazione recensioni------------------#
        rece1 = Recensione.objects.create(
            film=test_film1,
            utente=test_user,
            voto=4,
            commento_scritto='Commento...')

        rece2 = Recensione.objects.create(
            film=test_film2,
            utente=test_user,
            voto=2,
            commento_scritto='Commento...'
        )

        rece3 = Recensione.objects.create(
            film=test_film1,
            utente=other_user,
            voto=4,
            commento_scritto='Commento...')

        rece4 = Recensione.objects.create(
            film=test_film2,
            utente=other_user,
            voto=2,
            commento_scritto='Commento...'
        )

        rece5 = Recensione.objects.create(
            film=test_film3,
            utente=other_user,
            voto=2,
            commento_scritto='Commento...'
        )
        #-------------------------------------------------------#

        self.client = Client()
        session = self.client.session
        session['logged_user'] = test_user.username
        session.save()

        self.response = self.client.post('/streamify/account/')

    def test_account_recommended_system(self):
        self.assertEqual(self.response.status_code, 200)