"""Definition of all views."""

import uuid
import environ
from django.contrib import messages
from sslcommerz_lib import SSLCOMMERZ
from django.utils.http import urlencode
from django.contrib.auth.models import User
from .forms import SignupForm, CheckoutForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import FoodItem, Menu, Topping, Order, Size, AddOn, Status, Transaction
from django.core.paginator import Paginator

# Read env file
env = environ.Env()
environ.Env.read_env()

# SSLCOMMERZ config
sslcz = SSLCOMMERZ({
    "store_id": env("STORE_ID"),
    "store_pass": env("STORE_PASSWORD"),
    "issandbox": True
})


def index(request):
    """Home page."""
    foods = FoodItem.objects.all().order_by("id")
    # Show 5 foods per page
    paginator = Paginator(foods, 6)
    page_number = request.GET.get("page")
    food_obj = paginator.get_page(page_number)
    orders_count = Order.objects.filter(user=request.user.id, status=1).count()
    context = {"foods": food_obj, "orders_count": orders_count}
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


@login_required
def add_to_cart(request):
    """Add to cart."""
    if request.method == "POST":
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
        # TODO: HANDLE ERROR?
        current_order = Order(user=User.objects.get(pk=request.user.id),
                              food=FoodItem.objects.get(pk=food_id),
                              addon=AddOn.objects.get(addon_name=addon),
                              topping1=topping_1,
                              topping2=topping_2,
                              topping3=topping_3,
                              extra_cheese=extra_cheese,
                              size=size,
                              price=price,
                              status=Status.objects.get(pk=1))
        current_order.save()
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


@login_required
def my_orders_view(request):
    """
    View cart items.

    We display all orders that were submitted and are pending.
    """
    orders = Order.objects.filter(
        user=request.user.id).order_by("-id").exclude(status=1)
    # Show 5 orders per page
    paginator = Paginator(orders, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    orders_count = Order.objects.filter(user=request.user.id, status=1).count()
    context = {
        "orders": page_obj,
        "orders_count": orders_count
    }
    return render(request, "orders/my_orders.html", context)


@login_required
def checkout(request):
    """Checkout."""
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        # Get session key if form is valid
        if form.is_valid():
            num_of_item = request.session["num_of_item"]
            total_amount = request.session["total_price"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            address = form.cleaned_data["address"]
            tran_id = uuid.uuid4().int
            response = sslcz.createSession({
                'total_amount': total_amount,
                'currency': "USD",
                # unique transaction id
                'tran_id': tran_id,
                # if transaction is succesful, user will be redirected here
                'success_url': "http://127.0.0.1:8000/successful-payment-listener",
                # if transaction is failed, user will be redirected here
                'fail_url': "http://127.0.0.1:8000/unsuccessful-payment-listener",
                # after user cancels the transaction, will be redirected here
                'cancel_url': "http://127.0.0.1:8000/cart",
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
            # TODO: Save the session key if needed and redirect to PG page
            if response["status"] == "SUCCESS":
                # Save transaction information in db
                cur_transaction = Transaction(user=User.objects.get(pk=request.user.id),
                                              name=request.user.get_username(),
                                              email=email,
                                              phone=phone,
                                              amount=total_amount,
                                              address=address,
                                              status="pending",
                                              transaction_id=tran_id,
                                              currency="USD")
                cur_transaction.save()
                return redirect(response['GatewayPageURL'])
            else:
                messages.error(
                    request, "Sorry, there was an error. Please try again.")
                form = CheckoutForm()
                return redirect("/checkout")
        else:
            return render(request, "orders/checkout.html", {"form": form})
    form = CheckoutForm()
    # List of values received from query parameters
    msgs = request.GET.values() if len(request.GET.keys()) > 0 else []
    context = {
        "total_price": request.session["total_price"] if "total_price" in request.session else 0,
        "form": form,
        "messages": msgs
    }
    return render(request, "orders/checkout.html", context)


@csrf_exempt
def successful_payment_listener(request):
    """Listener for successful payment"""
    if request.method == "POST":
        if sslcz.hash_validate_ipn(request.POST):
            if request.POST["status"] == "VALID":
                response = sslcz.validationTransactionOrder(
                    request.POST["val_id"])
                if (response["status"] ==
                        "VALID" or response["status"] == "VALIDATED"):
                    # Update transaction db
                    try:
                        tran_id = request.POST["tran_id"]
                        trans_info = Transaction.objects.get(
                            transaction_id=tran_id)
                        trans_info.status = "processing"
                        trans_info.save()
                        return redirect("/successful-payment-view?" +
                                        urlencode({
                                            "tran_id": tran_id
                                        }))
                    except Transaction.DoesNotExist:
                        return redirect(
                            "/checkout?" + urlencode({
                                "msg": "No transaction information found"
                            }))
                else:
                    return redirect("/unsuccessful-payment-view")
            elif request.POST["status"] == "FAILED":
                return redirect(
                    "/checkout?" + urlencode({
                        "msg": "Your transaction is declined by your Bank"
                    }))
            elif request.POST["status"] == "CANCELLED":
                return redirect(
                    "/checkout?" + urlencode({
                        "msg": "You cancelled the transaction"
                    }))
            elif request.POST["status"] == "UNATTEMPTED":
                return redirect(
                    "/checkout?" + urlencode({
                        "msg": "You didn't choose any payment channel"
                    }))
            else:
                return redirect(
                    "/checkout?" + urlencode({"msg": "Payment Timeout"}))
        else:
            return redirect(
                "/checkout?" + urlencode({"msg": "Hash validation failed"}))
    return redirect("/")


def successful_payment_view(request):
    """View to be displayed when payment is successful"""
    if request.user.is_authenticated:
        # Confirm orders
        new_orders = Order.objects.filter(
            user=request.user.id, status=1)
        for order in new_orders:
            order.status = Status.objects.get(pk=2)
        Order.objects.bulk_update(new_orders, ["status"])
        return render(request, "orders/success.html")
    return redirect("/")


@csrf_exempt
def unsuccessful_payment_listener(request):
    """Listener for unsuccessful payment"""
    if request.method == "POST":
        return redirect("/unsuccessful-payment-view")
    return redirect("/")


def unsuccessful_payment_view(request):
    """View to be displayed when payment is unsuccessful"""
    if request.user.is_authenticated:
        return render(request, "orders/failure.html")
    return redirect("/")


def delete_order(request):
    """Delete an order."""
    if request.user.is_authenticated and request.method == "POST":
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
    if request.user.is_superuser:
        orders = Order.objects.order_by("-id").exclude(status=1)
        # Show 5 orders per page
        paginator = Paginator(orders, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "orders/admin_orders.html", {"orders": page_obj})
    return redirect("/")


def order_confirmation_admin(request):
    """Order confirmaiton by supersuer."""
    if request.user.is_superuser and request.method == "POST":
        order_id = request.POST["orderId"]
        order = Order.objects.get(pk=order_id)
        order.status = Status.objects.get(pk=3)
        order.save()
        return JsonResponse({"updated": True})
    return redirect("/")
