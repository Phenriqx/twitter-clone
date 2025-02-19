from django.test import TestCase, SimpleTestCase
from base.models import *
from django.urls import reverse

class TestHomePage(SimpleTestCase):
    
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        

class TestProfilePage(TestCase):
    
    def test_profile_page_redirects_anonymous_users(self):
        response = self.client.get(reverse('link-profile', kwargs={'username': 'testuser'}))
        self.assertRedirects(response,
                             expected_url=f"{reverse('login')}?next={reverse('link-profile', kwargs={'username': 'testuser'})}"
        )
    
    def test_profile_page_accessible_for_authenticated_users(self):
        User.objects.create(username='testuser', name='test', email='test@gmail.com')
        
        self.client.login(username='testuser', name='test', email='test@gmail.com')
        response = self.client.get(reverse('link-profile', kwargs={'username': 'testuser'}))
        
        self.assertEqual(response.status_code, 302)