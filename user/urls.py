# Import the path function to define URL routes in the application.
from django.urls import path

# Import the views module from the user app to connect views with URL patterns.
from user import views

# Define the list of URL patterns for user-related operations.
urlpatterns = [
    # URL pattern for the user dashboard; uses UserDashboardView class-based view.
    # URL: /user/dashboard, Name: dashboard.
    path("dashboard", views.UserDashboardView.as_view(), name="dashboard"),

    # URL pattern to add a new user; uses UserCreateView.
    # URL: /user/add/, Name: add-user.
    path("add/", views.UserCreateView.as_view(), name="add-user"),

    # URL pattern to list all users; uses UserListView.
    # URL: /user/all/, Name: all-users.
    path("all/", views.UserListView.as_view(), name="all-users"),

    # URL pattern to update a user's profile information using primary key (pk).
    # URL: /user/update-profile/<pk>/, Name: update-profile.
    path("update-profile/<int:pk>/", views.UserUpdateProfileView.as_view(), name="update-profile"),

    # URL pattern to update a user using primary key (pk).
    # URL: /user/update/<pk>/, Name: update-user.
    path("update/<int:pk>/", views.UserUpdateView.as_view(), name="update-user"),

    # URL pattern for a user to change their current password.
    # URL: /user/change-password/, Name: change-password.
    path("change-password/", views.UserChangePasswordView.as_view(), name="change-password"),

    # URL pattern to set a new password directly.
    # URL: /user/set-password/, Name: set-password.
    path("set-password/", views.UserSetPasswordView.as_view(), name="set-password"),

    # URL pattern to log out the currently authenticated user.
    # URL: /user/logout/, Name: logout.
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
]