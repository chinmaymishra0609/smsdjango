from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from user.views import UserLoginView, UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView
from core import views

urlpatterns = [
    path("", view=UserLoginView.as_view(), name="login"),
    path("password-reset/", view=UserPasswordResetView.as_view(), name="password-reset"),
    path("password-reset-done/", view=UserPasswordResetDoneView.as_view(), name="password-reset-done"),
    path("password-reset-confirm/<uidb64>/<token>/", view=UserPasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("password-reset-complete/", view=UserPasswordResetCompleteView.as_view(), name="password-reset-complete"),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("student/", include("student.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)