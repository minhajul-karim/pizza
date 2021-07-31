"""Class definitions of Forms."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields


class SignupForm(UserCreationForm):
    """Class for sign up form."""

    email = forms.EmailField()

    class Meta:
        """Meta class."""

        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]

    def clean_email(self, *args, **kwargs):
        """Validate unique email address."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A user with that email already exists.")
        return email


class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username"
        ]


class CheckoutForm(forms.Form):
    """Class for checkout form."""

    email = forms.EmailField(label="Email address")
    phone = forms.CharField(label="Phone number", min_length=5)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
