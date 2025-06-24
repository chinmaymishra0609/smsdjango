from django.urls import path
from user import views

urlpatterns = [
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("change-password/", views.UserChangePasswordView.as_view(), name="change-password"),
    path("set-password/", views.UserSetPasswordView.as_view(), name="set-password"),
]