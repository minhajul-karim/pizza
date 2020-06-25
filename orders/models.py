"""Definition of Database models."""

from django.db import models


class FoodItem(models.Model):
    """The class to contain food items."""

    food_name = models.CharField(max_length=100)
    food_image = models.CharField(max_length=1000, default="abc")

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


class Price(models.Model):
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


class Order(models.Model):
    """The class to contain orders."""

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
    extra_cheese = models.CharField(max_length=5, default="No")
    size = models.ForeignKey(Size,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10,
                                decimal_places=2)

    def __str__(self):
        """Object representation of Order class."""
        return f"{self.food} - {self.total}"
