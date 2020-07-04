from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup_view, name="signup_view"),
    path("regular-pizza/<int:food_id>",
         views.product_view, name="sicillian-pizza"),
    path("sicillian-pizza/<int:food_id>",
         views.product_view, name="regular_pizza"),
    path("subs/<int:food_id>",
         views.product_view, name="subs"),
    path("pasta/<int:food_id>",
         views.product_view, name="pasta"),
    path("salads/<int:food_id>",
         views.product_view, name="salads"),
    path("dinner-platters/<int:food_id>",
         views.product_view, name="dinner-platters"),
    path("tell-price", views.price, name="tell_price"),
    path("add-to-cart", views.add_to_cart, name="add_to_cart"),
    path("cart", views.cart_view, name="cart"),
    path("confirm-order", views.confirm_order_view, name="confirm_order"),
    path("delete-order", views.delete_order, name="delete_order"),
    path("my-orders", views.my_orders_view, name="my_orders"),
    path("orders-admin", views.order_admin_view, name="orders_admin"),
    path("confirm-order-admin", views.order_confirmation_admin,
         name="confirm_order_admin"),
]
