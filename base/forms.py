from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, Comment, List


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
                'placeholder': "Post your reply",
                'class': 'input__Text',
                'autocomplete':'off',
                })
        }
        

class ListForm(forms.ModelForm):
    
    class Meta:
        model = List
        exclude = ['author', 'participants']
        widgets = {
            'topic': forms.TextInput(attrs={
                'placeholder': "Topic",
                'class': 'input__Text list__Input',
                'autocomplete':'off',
                }),
            'name': forms.TextInput(attrs={
                'placeholder': "List name",
                'class': 'input__Text list__Input',
                'autocomplete':'off',
                }),
            'description': forms.Textarea(attrs={
                'placeholder': "List description",
                'class': 'input__Text input__Textarea',
                'autocomplete':'off',
                }),
        }