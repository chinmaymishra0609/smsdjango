from django.urls import path
from user import views

urlpatterns = [
    path("dashboard", views.UserDashboardView.as_view(), name="dashboard"),
    path("add/", views.UserCreateView.as_view(), name="add-user"),
    path("all/", views.UserListView.as_view(), name="all-users"),
    path("update-profile/<int:pk>/", views.UserUpdateProfileView.as_view(), name="update-profile"),
    path("update/<int:pk>/", views.UserUpdateView.as_view(), name="update-user"),
    path("change-password/", views.UserChangePasswordView.as_view(), name="change-password"),
    path("set-password/", views.UserSetPasswordView.as_view(), name="set-password"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
]