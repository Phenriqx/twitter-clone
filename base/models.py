from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    #media = models.ImageField()
    
    class Meta:
        abstract = False

    def __str__(self):
        return self.name
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
class Post(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #media 
    
    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return f'{self.id} - {self.author}: {self.content[:50] if len(self.content) > 50 else self.content}'
    

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
    topic = models.CharField(max_length=80, blank=False)
    
    def __str__(self):
        return self.topic     
           
class List(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'The list {self.name} created by {self.author.username} with topic {self.topic}; id: {self.id}; participants: {self.participants}'
    
    
class Message(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    
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