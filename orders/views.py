"""View of index page."""

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from .models import FoodItem, Menu, Topping


def index(request):
    """Home page."""
    foods = FoodItem.objects.all()
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


def product_view(request, food_id):
    """View product page.

    We get the food id via argument and grab menu for that food.
    Then we make lists of addons and sizes, remove duplicates from them
    and render the product page.
    """
    menu = Menu.objects.filter(food=food_id)
    image = FoodItem.objects.get(pk=food_id).food_image
    addons = [food.addon for food in menu]
    addons = list(set(addons))
    sizes = [food.size for food in menu]
    sizes = list(set(sizes))
    # We make sizes[] & toppings[] empty
    # if a food doesn't come with any sizes or toppings or both
    if len(sizes) == 1 and sizes[0] is None:
        sizes = []
    if food_id == 1 or food_id == 2:
        toppings = Topping.objects.all()
    else:
        toppings = []
    context = {
        "food": menu[0].food,
        "image": image,
        "addons": addons,
        "toppings": toppings,
        "sizes": sizes
    }
    return render(request, "orders/product.html", context)


def test(request):
    if request.method == "POST":
        food_id = request.POST["foodId"]
        addon_id = request.POST["addonId"]
        size_id = request.POST["sizeId"]
        if size_id == "null":
            size_id = None
        price = Menu.objects.filter(
            food=food_id,
            addon=addon_id,
            size=size_id)[0].price
        return JsonResponse({"price": price})
    else:
        return JsonResponse({"status": "Invalid request."})
