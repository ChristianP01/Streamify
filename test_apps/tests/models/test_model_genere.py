from streamify.models import Genere
from django.test import TestCase

class TestModelGenere(TestCase):

    def setUp(self):

        self.test_genere = Genere.objects.create(
            name = "Avventura"
        )

        
    def test_model_genere(self):
        self.assertEqual(self.test_genere.__str__(), 'Avventura')