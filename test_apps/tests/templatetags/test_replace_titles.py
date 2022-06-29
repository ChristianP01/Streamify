from django.test import TestCase
from streamify.templatetags.replace_titles import replace_titles

class TestLoginSuccess(TestCase):

    def setUp(self):
        self.example_title = "Titolo_del_film"
        
    def test_login_success(self):
        self.assertEqual(replace_titles(self.example_title), "Titolo del film")