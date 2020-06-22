"""Customizes the admin interface."""

from django.contrib import admin
from . models import FoodItem, Topping, Size, AddOn, Price, Order

admin.site.register(FoodItem)
admin.site.register(Topping)
admin.site.register(Size)
admin.site.register(AddOn)
admin.site.register(Price)
admin.site.register(Order)
