# Import the Django admin module to include the admin interface in the URL patterns.
from django.contrib import admin

# Import Django's settings module to access project settings (used later for serving media files).
from django.conf import settings

# Import a helper function to serve media files during development.
from django.conf.urls.static import static

# Import the path and include functions for defining URL patterns.
from django.urls import path, include

# Import custom views for user login and password reset functionality from the user app.
from user.views import (
    UserLoginView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView, 
    UserPasswordResetCompleteView
)

# Define the list of URL patterns for the project.
urlpatterns = [
    # URL pattern for the login page using a class-based view.
    path("", view=UserLoginView.as_view(), name="login"),

    # URL pattern for the password reset request page.
    path("password-reset/", view=UserPasswordResetView.as_view(), name="password-reset"),

    # URL pattern shown after the password reset email has been sent.
    path("password-reset-done/", view=UserPasswordResetDoneView.as_view(), name="password-reset-done"),

    # URL pattern for confirming the password reset using uid and token from the email link.
    path("password-reset-confirm/<uidb64>/<token>/", view=UserPasswordResetConfirmView.as_view(), name="password-reset-confirm"),

    # URL pattern shown after the user has successfully reset their password.
    path("password-reset-complete/", view=UserPasswordResetCompleteView.as_view(), name="password-reset-complete"),

    # URL pattern for accessing the Django admin panel.
    path("admin/", admin.site.urls),

    # Include URL patterns defined in the user app.
    path("user/", include("user.urls")),

    # Include URL patterns defined in the student app.
    path("student/", include("student.urls")),
]

# Check if the Django project is running in DEBUG mode (i.e., development mode).
if settings.DEBUG:
    # Serve media files (like uploaded images, PDFs, etc.) through Django's development server.
    # This maps URLs starting with MEDIA_URL to the MEDIA_ROOT directory.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Serve static files (like CSS, JS, images) through Django's development server.
    # This maps URLs starting with STATIC_URL to the STATIC_ROOT directory.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)