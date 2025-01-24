from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author']