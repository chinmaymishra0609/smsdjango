from django.urls import path
from student import views

urlpatterns = [
    path("add/", views.StudentCreateView.as_view(), name="add-student"),
    path("all/", views.StudentListView.as_view(), name="all-students"),
    path("update/<int:pk>", views.StudentUpdateView.as_view(), name="update-student"),
    path("detail/<int:pk>", views.StudentDetailView.as_view(), name="get-student"),
    path("delete/<int:pk>", views.StudentDeleteView.as_view(), name="delete-student"),
]