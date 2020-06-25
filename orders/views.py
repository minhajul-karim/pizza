"""View of index page."""

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, AuthenticationForm
from .models import FoodItem, Price, Topping

# Create your views here.


def index(request):
    """Home page."""
    foods = FoodItem.objects.all()
    print(foods)
    return render(request, "orders/index.html", {"foods": foods})


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


def regular_pizza_view(request):
    """View for regular pizzas."""
    foods = Price.objects.filter(food=1)
    addons = [food.addon.addon_name for food in foods]
    addons = list(set(addons))
    addons.sort()
    toppings = Topping.objects.all()
    print(toppings)
    context = {
        "addons": addons,
        "toppings": toppings,
    }
    return render(request, "orders/reg_pizza.html", context)
