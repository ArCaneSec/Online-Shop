from django.shortcuts import render

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created

# Create your views here.


def order_create(request):
    """
    This view is responsible for creating an order via OrderCreateForm form.
    If request method is not `POST`, returning a raw form for creating form.
    """
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            # Launching async task to send succesful message email.
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            order_created.delay(order.id)
        return render(request, "orders/order/created.html", {"order": order})
    else:
        form = OrderCreateForm()
    return render(
        request, "orders/order/create.html", {"form": form, "cart": cart}
    )
