# Import the path function to define URL patterns.
from django.urls import path

# Import the views module from the student app to reference view classes.
from student import views

# Define the list of URL patterns specific to student-related operations.
urlpatterns = [
    # URL pattern for adding a new student using the StudentCreateView class-based view.
    path("add/", views.StudentCreateView.as_view(), name="add-student"),

    # URL pattern to display a list of all students using the StudentListView class-based view.
    path("all/", views.StudentListView.as_view(), name="all-students"),

    # URL pattern to update an existing student based on primary key (pk) using StudentUpdateView.
    path("update/<int:pk>", views.StudentUpdateView.as_view(), name="update-student"),

    # URL pattern to retrieve details of a specific student by primary key using StudentDetailView.
    path("detail/<int:pk>", views.StudentDetailView.as_view(), name="get-student"),

    # URL pattern to delete a student by primary key using StudentDeleteView.
    path("delete/<int:pk>", views.StudentDeleteView.as_view(), name="delete-student"),
]