import os

from celery import Celery

# Set the default django setting for celery.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Creating instance of the application.
app = Celery("config")

# Loading all custom configuration.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto discovering all async tasks.
app.autodiscover_tasks()
