import os
from celery import Celery

# Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smsdjango.settings")

# Celery app create.
app = Celery("smsdjango")

# Load config from Django settings.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in this module.
app.autodiscover_tasks()