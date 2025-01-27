from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': "What's happening?",
                'class': 'input__Text'
                }),
        }