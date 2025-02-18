from django.test import TestCase
from base.models import *

class TestPostModel(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        self.post = Post(id=1, author=user, content='Hello world!')
    
    def test_string_representation(self):
        self.assertEqual(str(self.post), '1 - testuser: Hello world!')
        
    def test_post_creation(self):
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(self.post.author, User.objects.get(username='testuser'))
        self.assertEqual(self.post.content, 'Hello world!')
        
    def test_post_content_is_not_none(self):
        self.post.content = ''
        with self.assertRaises(ValidationError):
            self.post.validate_post()
            
    def test_post_content_is_not_above_max_length(self):
        self.post.content = 'a' * 257
        with self.assertRaises(ValidationError):
            self.post.validate_post()