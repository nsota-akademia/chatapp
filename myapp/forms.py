from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from .models import CustomUser,Messages

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username","email","password1","password2","file")


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username","password")

class MessagesForm(forms.Form):
    message = forms.CharField(
        max_length = 200,
    )

    
    
    

