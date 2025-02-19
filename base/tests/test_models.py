from django.test import TestCase
from base.models import *

class TestPostModel(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(username='testuser')
        cls.post = Post(id=1, author=cls.user, content='Hello world!')
    
    def test_string_representation(self):
        self.assertEqual(str(self.post), '1 - testuser: Hello world!')
        
    def test_post_creation(self):
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(self.post.author, User.objects.get(username='testuser'))
        self.assertEqual(self.post.content, 'Hello world!')
        
    def test_post_content_is_not_none(self):
        post = Post.objects.create(id=1, author=self.user, content='')
        with self.assertRaises(ValidationError):
            post.validate_post()
            
    def test_post_content_is_not_above_max_length(self):
        post = Post.objects.create(id=1, author=self.user, content='a' * 257)
        with self.assertRaises(ValidationError):
            post.validate_post()