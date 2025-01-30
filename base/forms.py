from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, Comment


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': "What's happening?",
                'class': 'input__Text',
                'autocomplete':'off',
                })
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'post']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': "Ppst your reply",
                'class': 'input__Text',
                'autocomplete':'off',
                })
        }