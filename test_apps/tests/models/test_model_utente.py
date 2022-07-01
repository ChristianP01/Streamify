from streamify.models import Utente
from django.test import TestCase

class TestModelFilm(TestCase):

    def setUp(self):

        self.test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test'
        )


    def test_model_film(self):
        self.assertEqual(self.test_user.__str__(), "Utente testUser, avente e-mail test@test.it.")