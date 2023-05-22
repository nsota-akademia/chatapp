from django import forms
from .models import CustomUser
from allauth.account.forms import SignupForm,ChangePasswordForm


class CustomSignupForm(SignupForm):
    file = forms.ImageField(required=True)    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.file = self.cleaned_data["file"]
        user.save()
        return user

class MessagesForm(forms.Form):
    message = forms.CharField(
        max_length = 200,
    )

class CustomPasswordChangeForm(ChangePasswordForm):
    class Meta:
        model = CustomUser
        fields = ("old_password","new_password1","new_password2")

class SearchForm(forms.Form):
    friend_name = forms.CharField(
        max_length=200,
        required=False
    )
