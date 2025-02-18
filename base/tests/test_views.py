from django.test import TestCase, SimpleTestCase
from base.models import *
from django.urls import reverse

class TestHomePage(SimpleTestCase):
    
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)