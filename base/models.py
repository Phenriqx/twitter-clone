from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    
    username = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/', default='default.jpg')
    
    def validate_user(self):
        if len(self.username) == 0 or len(self.username) > 64:
            raise ValidationError('The username must be between 3 and 64 characters long.')
        if not self.username.isalnum():
            raise ValidationError('The username can only contain alphanumeric characters.')
        return self.username
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = False
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class Post(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def validate_post(self):
        if len(self.content) > 256:
            raise ValidationError('The post content cannot exceed 256 characters.')
        if not self.content.strip():
            raise ValidationError('The post content cannot be empty.')
        return self.content
    
    @property
    def get_likes(self) -> int:
        return Like.objects.filter(post=self).count()
    
    @property
    def get_reposts(self) -> int:
        return Repost.objects.filter(post=self).count()
    
    @property
    def get_comments(self):
        return Comment.objects.filter(post=self)
        
    def __str__(self):
        return f'{self.id} - {self.author.username}: {self.content[:50] if len(self.content) > 50 else self.content}'
    
    class Meta:
        ordering = ['-updated', '-created']
    

class Repost(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return f'The user {self.author} reposted the post {self.post.content}; id {self.post.id}'
        

class Like(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return f'The user {self.author} liked the post {self.post.content}; id {self.post.id}'

        

class Comment(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return f'{self.author.id} - {self.author}: {self.content[:50] if len(self.content) > 50 else self.content}; id: {self.id}'
    
    
class Bookmark(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self): 
        return f"""The user {self.user.username} bookmarked the post: 
                {self.post.content if len(self.post.content) < 50 else self.post.content} / id: {self.post.id}
                bookmarkd_id: {self.id}"""
                

class Topic(models.Model):
    topic = models.CharField(max_length=64, blank=False)
    
    def validate_topic(self):
        if len(self.topic) > 80:
            raise ValidationError('The topic name cannot exceed 80 characters.')
        if not self.topic.strip():
            raise ValidationError('The topic name cannot be empty.')
        return self.topic.strip()
    
    def __str__(self):
        return self.topic     
           
class List(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def validate_list(self):
        if len(self.name) > 100:
            raise ValidationError('The list name cannot exceed 100 characters.')
        if not self.name.strip():
            raise ValidationError('The list name cannot be empty.')
        return self.name.strip()
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'The list {self.name} created by {self.author.username} with topic {self.topic}; id: {self.id}; participants: {self.participants}'
    
    
class Message(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    
    def validate_message(self):
        if len(self.content) > 256:
            raise ValidationError('The message content cannot exceed 250 characters.')
        if not self.content.strip():
            raise ValidationError('The message content cannot be empty.')
        return self.content.strip()
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return f'message: {self.content if len(self.content) < 50 else self.content[:50]}; author: {self.author}; message_id {self.id}; list {self.list.name}'
    
class Follow(models.Model):
    
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'The user {self.follower.username} started following {self.following.username}' 