from django.test import Client, TestCase

class TestHomepage(TestCase):

    def setUp(self):

        self.client = Client()
        self.response = self.client.get('/streamify/home/')
        
    def test_homepage(self):
        self.assertEqual(self.response.status_code, 200)