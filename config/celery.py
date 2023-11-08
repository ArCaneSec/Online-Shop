import os

from celery import Celery

# Set the default django setting for celery.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Creating instance of the application.
broker_url = "amqp://arcane:123@localhost:5672"
app = Celery("myshop", broker=broker_url)

# Loading all custom configuration.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto discovering all async tasks.
app.autodiscover_tasks()
