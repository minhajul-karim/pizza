"""Class definitions of Forms."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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
