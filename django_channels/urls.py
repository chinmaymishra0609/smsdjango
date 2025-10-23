# Import the path function to define URL routes in the application.
from django.urls import path
# Import the views module from the user app to connect views with URL patterns.
from . import views

# Define the list of URL patterns for user-related operations.
urlpatterns = [
    path("chat/<str:group_name>/", views.ChatView.as_view(), name="chat-view"),
]