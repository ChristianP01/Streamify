import email
from streamify.models import Utente
from django.test import TestCase

class TestModelUtente(TestCase):

    def setUp(self):

        self.test_user = Utente.objects.create(
            username='testUser',
            password='testUser',
            email='test@test.it',
            nome='Test',
            cognome='test'
        )

        self.test_user.set_password('testUser')
        self.test_user.save()


    def test_model_utente(self):
        self.assertEqual(self.test_user.__str__(), "Utente testUser, avente e-mail test@test.it.")

    def test_create_user(self):
        self.assertIsInstance(self.test_user, Utente)

    def test_user_is_active(self):
        self.assertTrue(self.test_user.is_active)