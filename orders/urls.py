from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup_view, name="signup_view"),
    path("regular-pizza", views.regular_pizza_view, name="regular_pizza_view"),
]
