from django.test import Client, TestCase

class TestCatalogoSuccess(TestCase):

    def setUp(self):

        self.client = Client()
        self.response = self.client.get('/streamify/catalogo/')

    def test_catalogo_success(self):
        self.assertEqual(self.response.status_code, 200)