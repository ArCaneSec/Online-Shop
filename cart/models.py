from decimal import Decimal

from django.conf import settings
from django.db import models
from django.http import HttpRequest

from shop.models import Product

# Create your models here.


class Cart:
    """This class is responsible for handling cart functionality
    and storing it in users session.
    """

    def __init__(self, request: HttpRequest) -> None:
        """Initializing the cart class"""
        self.session = request.session
        self.cart: dict = self.session.get(settings.CART_SESSION_ID, {})

    def __str__(self) -> str:
        return super().__str__()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Count all items in the cart"""
        return sum(item["quantity"] for item in self.cart.values())

    def add(
        self,
        product: Product,
        quantity: int = 1,
        override_quantity: bool = False,
    ):
        """This method will add a product to cart, or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        """
        This method will tell django that the session
        has changed and needs to be updated
        """
        self.session.modified = True

    def remove(self, product):
        """
        Removing a product from current session(cart)
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self) -> Decimal:
        """Counting total price of current cart.

        Return:
            total price
        """
        return sum(
            Decimal(product["price"]) * product["quantity"]
            for product in self.cart.values()
        )

    def clear(self):
        """Deleting all items in cart"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
