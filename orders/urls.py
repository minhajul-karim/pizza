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
    path("tell_price", views.price),
]
