from django import forms
from .models import CustomUser
from allauth.account.forms import SignupForm, ChangePasswordForm


class CustomSignupForm(SignupForm):
    file = forms.ImageField(required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        if user:
            user.file = self.cleaned_data["file"]
            user.save()
        return user


class MessagesForm(forms.Form):
    message = forms.CharField(
        max_length=200,
        required=False,
    )


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username",)


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomPasswordChangeForm(ChangePasswordForm):
    class Meta:
        model = CustomUser
        fields = ("old_password", "new_password1", "new_password2")


class SearchForm(forms.Form):
    search = forms.CharField(max_length=200, required=False, label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["search"].widget.attrs.update(
            {"placeholder": "Search by email or username"}
        )
