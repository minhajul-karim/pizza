"""Definition of Database models."""

from django.db import models
from django.conf import settings


class FoodItem(models.Model):
    """The class to contain food items."""

    food_name = models.CharField(max_length=100)
    food_image = models.CharField(max_length=1000, default="")
    slug = models.CharField(max_length=100, default="")

    def __str__(self):
        """Object representation of Fooditem class."""
        return f"{self.food_name}"


class Size(models.Model):
    """The class to contain sizes of food items."""

    size_name = models.CharField(max_length=10)

    def __str__(self):
        """Object representation of Size class."""
        return f"{self.size_name}"


class AddOn(models.Model):
    """The class to contain add-ons."""

    addon_name = models.CharField(max_length=200)

    def __str__(self):
        """Object representation of Addon class."""
        return f"{self.addon_name}"


class Topping(models.Model):
    """The class to contain pizza toppings."""

    topping_name = models.CharField(max_length=100)

    def __str__(self):
        """Object representation of Topping class."""
        return f"{self.topping_name}"


class Status(models.Model):
    """The class to contain order status."""

    status_name = models.CharField(max_length=50)

    def __str__(self):
        """Object representation of Status class."""
        return f"{self.status_name}"


class Menu(models.Model):
    """The class to contain price."""

    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    addon = models.ForeignKey(AddOn, on_delete=models.CASCADE)
    size = models.ForeignKey(
        Size, blank=True, null=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        """Constraint to make food, addon, & size unique."""

        constraints = [
            models.UniqueConstraint(
                fields=["food", "addon", "size"], name="unq_price")
        ]

    def __str__(self):
        """Object representation of Price class."""
        return f"{self.food} - {self.addon} - {self.size} - {self.price}"


class Transaction(models.Model):
    """The class to contain transaction information"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)
    name = models.CharField(max_length=255, default=None)
    email = models.CharField(max_length=30, default=None)
    phone = models.CharField(max_length=20, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    status = models.CharField(max_length=10, default=None)
    transaction_id = models.CharField(max_length=255, default=None)
    currency = models.CharField(max_length=20, default=None)

    def __str__(self):
        """Object representation of Transaction class."""
        return f"{self.transaction_id} - {self.name} \
            - {self.amount} - {self.status}"


class Order(models.Model):
    """The class to contain orders."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             default=0)
    food = models.ForeignKey(FoodItem,
                             on_delete=models.CASCADE)
    addon = models.ForeignKey(AddOn,
                              on_delete=models.CASCADE)
    topping1 = models.ForeignKey(Topping,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE,
                                 related_name="topping1")
    topping2 = models.ForeignKey(Topping,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE,
                                 related_name="topping2")
    topping3 = models.ForeignKey(Topping,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE,
                                 related_name="topping3")
    extra_cheese = models.CharField(max_length=5,
                                    blank=True,
                                    null=True,
                                    default="N")
    size = models.ForeignKey(Size,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    status = models.ForeignKey(Status,
                               on_delete=models.CASCADE,
                               default=1)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.PROTECT)

    def __str__(self):
        """Object representation of Order class."""
        return f"{self.food} - {self.price} - {self.status} \
             {self.transaction_id}"
