"""View of index page."""

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from .models import FoodItem, Menu, Topping, Order, Size, AddOn, Status
from django.contrib.auth.models import User


def index(request):
    """Home page."""
    foods = FoodItem.objects.all()
    orders_count = Order.objects.filter(user=request.user.id, status=1).count()
    context = {
        "foods": foods,
        "orders_count": orders_count,
    }
    return render(request, "orders/index.html", context)


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
    cheese_options = []
    toppings = []
    orders_count = Order.objects.filter(user=request.user.id, status=1).count()
    # We make sizes[] & toppings[] empty if a food
    # doesn't come with any sizes or toppings or both
    if len(sizes) == 1 and sizes[0] is None:
        sizes = []
    if food_id == 1 or food_id == 2:
        toppings = Topping.objects.all()
    if food_id == 3:
        cheese_options = [{
            "label": "Add extra cheese",
            "id": "cheese-yes",
            "value": "Y"
        },
            {
            "label": "No, I'm good",
            "id": "cheese-no",
            "value": "N"
        }]

    context = {
        "food": menu[0].food,
        "image": image,
        "addons": addons,
        "toppings": toppings,
        "cheese_options": cheese_options,
        "sizes": sizes,
        "orders_count": orders_count,
    }
    return render(request, "orders/product.html", context)


def price(request):
    """Tells the price to client."""
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


def add_to_cart(request):
    """Add to cart."""
    if request.method == "POST":
        if request.user.is_authenticated:
            food_id = request.POST["food-id"]
            addon = request.POST["addon"]
            topping_1 = Topping.objects.get(
                topping_name=request.POST["topping-1"]) if "topping-1" in request.POST else None
            topping_2 = Topping.objects.get(
                topping_name=request.POST["topping-2"]) if "topping-2" in request.POST else None
            topping_3 = Topping.objects.get(
                topping_name=request.POST["topping-3"]) if "topping-3" in request.POST else None
            size = Size.objects.get(
                size_name=request.POST["size"]) if "size" in request.POST else None
            price = request.POST["price"]
            extra_cheese = None
            if "cheese" in request.POST and request.POST.get("cheese") == "Y":
                extra_cheese = request.POST["cheese"]
            # Save data into db
            ord = Order(user=User.objects.get(pk=request.user.id),
                        food=FoodItem.objects.get(pk=food_id),
                        addon=AddOn.objects.get(addon_name=addon),
                        topping1=topping_1,
                        topping2=topping_2,
                        topping3=topping_3,
                        extra_cheese=extra_cheese,
                        size=size,
                        price=price,
                        status=Status.objects.get(pk=1))
            ord.save()
        else:
            return redirect("/login")
    return redirect("/")


def cart_view(request):
    """
    View cart items.

    We display all orders that weren't confirmed by user.
    """
    orders = Order.objects.filter(user=request.user.id, status=1)
    orders_count = Order.objects.filter(user=request.user.id, status=1).count()
    context = {
        "orders": orders,
        "orders_count": orders_count
    }
    return render(request, "orders/cart.html", context)


def my_orders_view(request):
    """
    View cart items.

    We display all orders that were submitted and are pending.
    """
    orders = Order.objects.filter(user=request.user.id, status=2)
    orders_count = Order.objects.filter(user=request.user.id, status=1).count()
    context = {
        "orders": orders,
        "orders_count": orders_count
    }
    return render(request, "orders/my_orders.html", context)


def confirm_order_view(request):
    """Order confirmation."""
    orders_not_confirmed = Order.objects.filter(user=request.user.id, status=1)
    for order in orders_not_confirmed:
        order.status = Status.objects.get(pk=2)
        order.save()
    return redirect("/")


def delete_order(request):
    """Delete an order."""
    if request.method == "POST":
        order_id = request.POST["orderId"]
        Order.objects.get(id=order_id).delete()
        remaining_orders = Order.objects.filter(
            user=request.user.id, status=1).count()
        return JsonResponse({"remaining_orders": remaining_orders})
    else:
        return JsonResponse({"status": "Invalid request."})
