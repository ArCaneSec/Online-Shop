from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product

from .forms import CartAddProductForm
from .models import Cart

# Create your views here.


@require_POST
def cart_add(request, product_id):
    """This view is responsible for add or updating a cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd["quantity"],
            override_quantity=cd["override"],
        )
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """Removing a product from existing cart."""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    "This view will provide a detailed information about user's cart"
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True}
        )
        cart.lab()
    return render(request, "cart/detail.html", {"cart": cart})
