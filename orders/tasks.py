import logging

from celery import shared_task
from django.core.mail import send_mail

from .models import Order

logger = logging.getLogger(__name__)


@shared_task
def order_created(order_id: int):
    """
    Async task executed by celery worker that send
    email messages to customer who have created an order.
    """
    try:
        logger.info(f"Processing order {order_id}")
        order = Order.objects.get(id=order_id)
        subject = f"Order nr. {order.id}"
        message = (
            f"Dear {order.first_name}\n\n"
            "you have successfully placed an order."
            f"your order id: {order.id}"
        )
        mail_sent = send_mail(
            subject,
            message,
            "admin@shop.com",
            [order.email],
            fail_silently=False,
        )

        logger.info(f"Mail sent: {mail_sent}")
        return mail_sent
    except Exception as e:
        logger.exception(f"Error processing order {order_id}: {e}")
        return False
