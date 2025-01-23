from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User

#User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']