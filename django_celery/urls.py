# Import the path function to define URL routes in the application.
from django.urls import path

# Import the views module from the user app to connect views with URL patterns.
from django_celery import views

# Define the list of URL patterns for user-related operations.
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("check-result/<str:task_id>", views.CheckResult.as_view(), name="check-result"),
]