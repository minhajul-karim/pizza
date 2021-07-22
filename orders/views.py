"""View of index page."""

import environ
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm, CheckoutForm
from .models import FoodItem, Menu, Topping, Order, Size, AddOn, Status
from django.contrib.auth.models import User
from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt

# Read env file
env = environ.Env()
environ.Env.read_env()

# SSLCOMMERZ config
sslcz = SSLCOMMERZ({
    "store_id": env("STORE_ID"),
    "store_pass": env("STORE_PASSWORD"),
    "issandbox": True
})

@csrf_exempt
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


def product_view(request, slug, food_id):
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

@csrf_exempt
def cart_view(request):
    """
    View cart items.

    We display all orders that weren't confirmed by user.
    """
    orders = Order.objects.filter(user=request.user.id, status=1)
    total_price = 0
    for order in orders:
        total_price += order.price
    orders_count = orders.count()
    request.session["total_price"] = str(total_price)
    request.session["num_of_item"] = orders_count
    context = {
        "orders": orders,
        "orders_count": orders_count,
        "total_price": total_price
    }
    return render(request, "orders/cart.html", context)


def my_orders_view(request):
    """
    View cart items.

    We display all orders that were submitted and are pending.
    """
    orders = Order.objects.filter(
        user=request.user.id).order_by("-id").exclude(status=1)
    orders_count = Order.objects.filter(user=request.user.id, status=1).count()
    context = {
        "orders": orders,
        "orders_count": orders_count
    }
    return render(request, "orders/my_orders.html", context)


def checkout(request):
    """Checkout."""
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            num_of_item = request.session["num_of_item"]
            total_amount = request.session["total_price"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            address = form.cleaned_data["address"]
            response = sslcz.createSession({
                'total_amount': total_amount,
                'currency': "USD",
                'tran_id': "tran_12345",
                'success_url': "http://127.0.0.1:8000/successful-payment", # if transaction is succesful, user will be redirected here
                'fail_url': "http://127.0.0.1:8000/unsuccessful-payment", # if transaction is failed, user will be redirected here
                'cancel_url': "http://127.0.0.1:8000/cart", # after user cancels the transaction, will be redirected here
                'emi_option': "0",
                'cus_name': "test",
                'cus_email': email,
                'cus_phone': phone,
                'cus_add1': address,
                'cus_city': "Dhaka",
                'cus_country': "Bangladesh",
                'shipping_method': "NO",
                'multi_card_name': "",
                'num_of_item': num_of_item,
                'product_name': "Test",
                'product_category': "Test Category",
                'product_profile': "general",
            })
            orders_not_confirmed = Order.objects.filter(user=request.user.id, status=1)
            for order in orders_not_confirmed:
                order.status = Status.objects.get(pk=2)
                order.save()
            return redirect(response['GatewayPageURL'])
        else:
            return render(request, "orders/checkout.html", {"form": form})
    else:
        form = CheckoutForm()
        context = {
            "total_price": request.session["total_price"],
            "form": form
        }
        return render(request, "orders/checkout.html", context)


def delete_order(request):
    """Delete an order."""
    if request.method == "POST":
        order_id = request.POST["orderId"]
        Order.objects.get(pk=order_id).delete()
        remaining_orders = Order.objects.filter(
            user=request.user.id, status=1)
        total_price = 0
        for order in remaining_orders:
            total_price += order.price
        return JsonResponse({"remaining_orders": remaining_orders.count(),
                             "total_price": total_price})
    else:
        return JsonResponse({"status": "Invalid request."})


def order_admin_view(request):
    """View admin interface of orders."""
    orders = Order.objects.order_by("-id").exclude(status=1)
    return render(request, "orders/admin_orders.html", {"orders": orders})

def order_confirmation_admin(request):
    """Order confirmaiton by supersuer."""
    if request.method == "POST":
        order_id = request.POST["orderId"]
        order = Order.objects.get(pk=order_id)
        order.status = Status.objects.get(pk=3)
        order.save()
        return HttpResponse("a")

@csrf_exempt
def successful_payment(request):
    """View to be displayed when payment is successful"""
    request.session["total_price"] = 0
    return render(request, "orders/success.html")

@csrf_exempt
def unsuccessful_payment(request):
    """View to be displayed when payment is unsuccessful"""
    return render(request, "orders/failure.html")

