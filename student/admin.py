# Import the Django admin module which provides a web interface for managing models.
from django.contrib import admin

# Import the Student model from the current app's models.py file.
from .models import Student

# Register the Student model with the Django admin site using a decorator.
# This is a cleaner alternative to admin.site.register(Student, StudentAdmin).
@admin.register(Student)

# Define a custom ModelAdmin class to configure how the Student model appears in the admin interface.
class StudentAdmin(admin.ModelAdmin):
    # Automatically display all fields of the Student model in the admin list view.
    # This uses a list comprehension to get the name of each field defined in the model's _meta API.
    list_display = [field.name for field in Student._meta.fields]