from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
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
class PasswordForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ("old_password","new_password1","new_password2")
    

