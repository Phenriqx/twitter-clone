from django.test import TestCase
from base.models import *


class TestCustomUserModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testuser', 
                                       name='Test User',
                                       email='testuser@gmail.com')
        
    def test_string_representation(self):
        self.assertEqual(str(self.user), 'Test User')
        
    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user, User.objects.get(username='testuser'))
        
    def test_username_is_not_none(self):
        user = User.objects.create(username='')
        with self.assertRaises(ValidationError):
            user.validate_user()
            
    def test_username_is_not_above_max_lenght(self):
        user = User.objects.create(username='a' * 65)
        with self.assertRaises(ValidationError):
            user.validate_user()

class TestPostModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
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
            
class TestLikeModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testuser')
        cls.post = Post.objects.create(author=cls.user, content='hello world')
        cls.like = Like.objects.create(author=cls.user, post=cls.post)
        
    def test_like_creation(self):
        self.assertTrue(isinstance(self.like, Like))
        self.assertEqual(self.like.author, User.objects.get(username='testuser'))
        self.assertEqual(self.like.post, Post.objects.get(content='hello world'))