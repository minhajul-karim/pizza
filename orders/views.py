"""View of index page."""

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, AuthenticationForm

# Create your views here.


def index(request):
    """Home page."""
    return render(request, "orders/index.html")


def signup_view(request):
    """Signup view."""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("index")
    else:
        form = SignupForm()

    return render(request, "orders/sign_up.html", {"form": form})
