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
        return f'{self.author.id} - {self.author}: {self.content[:50] if len(self.content) > 50 else self.content}'
    

class Repost(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        

class Like(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        

class Comment(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return f'{self.author.id} - {self.author}: {self.content[:50] if len(self.content) > 50 else self.content}'