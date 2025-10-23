import logging
from celery import Task
from django.utils import timezone
from smsdjango.celery import app
from time import sleep

# Logger setup.
logger = logging.getLogger(__name__)

class SendWelcomeEmailTask(Task):
    # Auto-retry configuration.
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3, "countdown": 30}
    retry_backoff = True
    name = "SendWelcomeEmailTask"

    def run(self, email, *args, **kwargs):
        logger.info(f"SendWelcomeEmailTask Started at {timezone.now()}.")

        logger.info(f"The email is being sent to {email}.")
        sleep(5)
        logger.info(f"The email has been sent to {email}.")

        logger.info(f"SendWelcomeEmailTask Finished at {timezone.now()}.")
        return True

# Register the task.
send_welcome_email_task = app.register_task(SendWelcomeEmailTask())

class ClearSessionCacheTask(Task):
    # Auto-retry configuration.
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3, "countdown": 30}
    retry_backoff = True
    name = "ClearSessionCacheTask"

    def run(self, *args, **kwargs):
        logger.info(f"ClearSessionCacheTask Started at {timezone.now()}.")

        logger.info(f"The cache is being cleared.")
        sleep(5)
        logger.info(f"The cache has been cleared.")

        logger.info(f"ClearSessionCacheTask Finished at {timezone.now()}.")
        return True

# Register the task.
clear_session_cache_task = app.register_task(ClearSessionCacheTask())