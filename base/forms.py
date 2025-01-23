from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

#User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'