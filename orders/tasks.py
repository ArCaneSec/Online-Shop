from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task()
def order_created(order_id: int):
    """
    This task is responsible to send notification via email
    whenever an order is created.
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order nr. {order.id}"
    message = (
        f"Dear {order.first_name}\n\n"
        "you have succesfully placed an order."
        f"your order id: {order.id}"
    )
    mail_sent = send_mail(subject, message, "admin@shop.com", [order.email], fail_silently=False)
    print("test")
    return mail_sent
