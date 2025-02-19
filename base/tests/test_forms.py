from django.test import TestCase
from base.forms import *
from django.urls import reverse
from base.models import *


class PostFormTest(TestCase):
    
    def test_create_post_when_submitting_validform(self):
        form_data = {
            'author': 'testuser',
            'content': 'hello world'
        }
        response = self.client.post(reverse('add-post'), data=form_data)
        self.assertEqual(response.status_code, 302)
        
    def test_dont_create_post_when_submitting_invalidform(self):
        form_data = {
            'author': 'testuser',
            'content': ''
        }
        response = self.client.post(reverse('add-post'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.exists())