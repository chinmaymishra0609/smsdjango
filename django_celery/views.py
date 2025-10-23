from django.shortcuts import render
from django.views import View
from celery.result import AsyncResult
from .tasks import send_welcome_email_task

class Home(View):
    context = {}

    def get(self, request, *args, **kwargs):
        self.context["result"] = send_welcome_email_task.delay("chinmaymishra0609@gmail.com")
        # self.context["result"] = send_welcome_email_task.apply_async(args=["mohitmishra.falna850@gmail.com"])

        return render(request=request, template_name="django_celery/home.html", context=self.context)

class CheckResult(View):
    context = {}

    def get(self, request, task_id=None, *args, **kwargs):
        self.context["result"] = AsyncResult(task_id)
        return render(request=request, template_name="django_celery/result.html", context=self.context)