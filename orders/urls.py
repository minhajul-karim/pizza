from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup_view, name="signup_view"),
    path("<str:slug>/<int:food_id>",
         views.product_view, name="sicillian-pizza"),
    path("tell-price", views.price, name="tell_price"),
    path("add-to-cart", views.add_to_cart, name="add_to_cart"),
    path("cart", views.cart_view, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("delete-order", views.delete_order, name="delete_order"),
    path("my-orders", views.my_orders_view, name="my_orders"),
    path("successful-payment", views.successful_payment, name="sucessful-payment"),
    path("unsuccessful-payment", views.unsuccessful_payment, name="unsucessful-payment"),
    path("orders-admin", views.order_admin_view, name="orders_admin"),
    path("confirm-order-admin", views.order_confirmation_admin,
         name="confirm_order_admin"),
]
