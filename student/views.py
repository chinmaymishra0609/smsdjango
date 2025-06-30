# Importing the `render` and `redirect` shortcuts to render templates and redirect users to different views.
from django.shortcuts import render, redirect

# Importing the base `View` class for creating class-based views.
from django.views import View

# Importing `reverse_lazy` to lazily reverse URLs (commonly used in class-based views where URL resolution needs to be delayed).
from django.urls import reverse_lazy

# Importing the custom form class `StudentForm` from the current app's forms module.
from .forms import StudentForm

# Importing Django's messaging framework to display success/error/info messages to users.
from django.contrib import messages

# Importing the `Student` model from the current app's models module.
from .models import Student

# Importing Django's `FileSystemStorage` class to handle file uploads and temporary file storage.
from django.core.files.storage import FileSystemStorage

# Importing paginator classes to divide a queryset into pages and handle pagination-related errors.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Importing the `LoginRequiredMixin` to restrict access to a view to authenticated users only.
from django.contrib.auth.mixins import LoginRequiredMixin

# Creating a file storage object that stores uploaded files in the `/tmp/` directory on the server.
file_storage = FileSystemStorage(location="/tmp/")

# Student create view here.
class StudentCreateView(LoginRequiredMixin, View):
    """
    A class-based view to handle the creation of Student records.

    This view:
    - Requires the user to be logged in (`LoginRequiredMixin`).
    - Displays a student creation form on GET request.
    - Handles form submission and student record creation on POST request.
    - Checks for the user's permission to add students.
    """

    # URL to redirect unauthenticated users to the login page.
    login_url = reverse_lazy("login")

    # A reusable dictionary to hold context data for rendering templates.
    context = {}

    def get(self, request):
        """
        Handles GET request to render the student creation form.

        - Checks if the user has permission to add a student.
        - If not, redirects to the dashboard with an error message.
        - Otherwise, renders the form with an appropriate title.
        """

        # If the user doesn't have permission to add a student, show an error and redirect.
        if not request.user.has_perm("student.add_student"):
            messages.error(request=request, message="You do not have permission to access this page.")
            return redirect("dashboard")

        # Set the page title in the context.
        self.context["title"] = "Add Student"

        # Add an instance of the StudentForm to the context (with no data).
        self.context["form"] = StudentForm(label_suffix="")

        # Render the template with the form.
        return render(request, "student/add-update-student.html", self.context)

    def post(self, request, *args, **kwargs):
        """
        Handles POST request to process and validate the student creation form.

        - Accepts form data and uploaded files.
        - Validates the form; if valid, saves the new student instance.
        - Shows success or error message based on the result.
        - Redirects to the same page after submission.
        - If the form is invalid, re-renders the form with errors.
        """

        # Create a form instance with POST data and FILES (for file uploads).
        self.context["form"] = StudentForm(request.POST, request.FILES, label_suffix="")

        # Check if the submitted form is valid.
        if self.context["form"].is_valid():
            # Save the form to create a Student object.
            student = self.context["form"].save()

            # If the student is saved successfully, show a success message.
            if student:
                messages.success(request=request, message="The record has been saved successfully.")
            else:
                # This branch is rare — save() normally returns the instance unless an exception occurs.
                messages.error(request=request, message="The record has not been saved. Try again.")

            # Redirect to the same form page after submission (possibly to add another student).
            return redirect("add-student")

        # If the form is invalid, re-render the form with validation errors.
        return render(request, "student/add-update-student.html", self.context)

# Student update view here.
class StudentUpdateView(LoginRequiredMixin, View):
    """
    A class-based view to handle updating an existing Student record.

    Features:
    - Requires the user to be logged in (via `LoginRequiredMixin`).
    - Checks for the 'change_student' permission.
    - On GET: Displays the update form pre-filled with student data.
    - On POST: Validates and saves the updated student data.
    """

    # URL to redirect unauthenticated users to the login page.
    login_url = reverse_lazy("login")

    # A shared context dictionary for rendering templates.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handles GET request to show the student update form.

        - Checks if user has permission to update student.
        - Fetches student by primary key (`pk`) from URL kwargs.
        - Renders the update form with pre-populated data.
        """

        try:
            # If the user lacks permission to update a student, show an error and redirect.
            if not request.user.has_perm("student.change_student"):
                messages.error(request=request, message="You do not have permission to access this page.")
                return redirect("dashboard")

            # Retrieve the student object by primary key (`pk`) from URL kwargs.
            student = Student.objects.get(pk=kwargs.get("pk"))

            # Set page title for the template.
            self.context["title"] = "Update Student"

            # Pass the student object to the context for use in the template.
            self.context["student"] = student

            # Create the form with the existing student instance (pre-filled with current data).
            self.context["form"] = StudentForm(instance=student, label_suffix="")

            # Render the form on the update page.
            return render(request, "student/add-update-student.html", self.context)

        # If the student does not exist (invalid ID or deleted), catch the exception.
        except Student.DoesNotExist:
            messages.error(request=request, message="The record does not exist or has already been deleted.")
            return redirect("all-students")

    def post(self, request, *args, **kwargs):
        """
        Handles POST request to process and save updated student data.

        - Retrieves the student instance by `pk`.
        - Binds form data and files to the form instance.
        - Validates the form and saves the updated student if valid.
        - Displays success/error messages accordingly.
        """

        # Retrieve the student instance to update using the primary key.
        student = Student.objects.get(pk=kwargs.get("pk"))

        # Bind submitted data and files to the form (with existing student instance).
        self.context["form"] = StudentForm(request.POST, request.FILES, instance=student, label_suffix="")

        # Check if the form is valid.
        if self.context["form"].is_valid():
            # Save the updated student object to the database.
            student = self.context["form"].save()

            # If student is saved successfully, show success message.
            if student:
                messages.success(request=request, message="The record has been updated successfully.")
            else:
                # Although rare, handle any issues during saving.
                messages.error(request=request, message="The record has not been updated. Try again.")

            # Redirect to the same update page to reflect changes or allow further edits.
            return redirect("update-student", pk=kwargs.get("pk"))

        # If form is invalid, re-render the page with error messages.
        return render(request, "student/add-update-student.html", self.context)

# Student list view here.
class StudentListView(LoginRequiredMixin, View):
    """
    A class-based view to list all Student records with pagination.

    Features:
    - Requires user authentication (via LoginRequiredMixin).
    - Checks for 'view_student', 'change_student', or 'delete_student' permission.
    - Supports dynamic pagination with 'per-page' query parameter.
    - Renders a paginated list of students in the template.
    """

    # Redirect unauthenticated users to the login page.
    login_url = reverse_lazy("login")

    # Shared context dictionary used for passing data to the template.
    context = {}

    def get(self, request):
        """
        Handles GET requests to display the student list.

        - Checks for proper permissions.
        - Parses 'per-page' and 'page' query parameters.
        - Applies pagination to the student queryset.
        - Renders the paginated student list in a template.
        """

        # Check if the user lacks all three permissions; if so, deny access and redirect.
        if not request.user.has_perm("student.view_student") \
           and not request.user.has_perm("student.change_student") \
           and not request.user.has_perm("student.delete_student"):
            messages.error(request=request, message="You do not have permission to access this page.")
            return redirect("dashboard")

        # Get the 'per-page' value from the URL query string (default is "10" if not provided).
        per_page = request.GET.get("per-page", "10")

        # Validate that per_page is a positive digit and within a sensible max limit.
        if not per_page.isdigit() or int(per_page) <= 0:
            # Fallback to default if invalid.
            per_page = 10
        else:
            # Limit maximum items per page to 100 to prevent excessive loads.
            per_page = min(int(per_page), 100)

        # Fetch all student records ordered by ID.
        student_lists = Student.objects.all().order_by("id")

        # Create a Paginator object to paginate the list with the per_page value.
        paginator = Paginator(student_lists, per_page)

        # Get the current page number from query parameters.
        current_page_number = request.GET.get("page")

        try:
            # Attempt to retrieve the desired page of students.
            students = paginator.page(current_page_number)
        except PageNotAnInteger:
            # If the page is not an integer, show the first page.
            students = paginator.page(1)
        except EmptyPage:
            # If the page number exceeds the total pages, show the last page.
            students = paginator.page(paginator.num_pages)

        # Add the paginated students list to the context.
        self.context["students"] = students

        # Add the current per-page setting to the context for template use.
        self.context["per_page"] = per_page

        # Set the page title for display in the template.
        self.context["title"] = "All Students"

        # Render the template with the context data.
        return render(request, "student/all-students.html", self.context)

# Student detail view here.
class StudentDetailView(LoginRequiredMixin, View):
    """
    A class-based view to display details of a single Student.

    Features:
    - Requires user authentication (`LoginRequiredMixin`).
    - Checks whether the user has permission to view student details.
    - Retrieves the student record by primary key (`pk`).
    - Handles cases where the student record does not exist.
    """

    # Specifies the URL to redirect unauthenticated users to the login page.
    login_url = reverse_lazy("login")

    # Shared context dictionary to pass data to the template.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display a student's detail page.

        - Checks for the 'view_student' permission.
        - Retrieves the student record using primary key (`pk`) from URL kwargs.
        - Passes the student object to the template for rendering.
        - If the student does not exist, shows an error message and redirects.
        """
        try:
            # If user lacks permission to view student details, show error and redirect.
            if not request.user.has_perm("student.view_student"):
                messages.error(request=request, message="You do not have permission to access this page.")
                return redirect("dashboard")

            # Set the page title in the context.
            self.context["title"] = "Student Details"

            # Retrieve the student record from the database using the primary key from the URL.
            self.context["student"] = Student.objects.get(pk=kwargs.get("pk"))

            # Render the student detail page with the context.
            return render(request, "student/get-student.html", self.context)

        # If the student with given primary key does not exist, handle the exception.
        except Student.DoesNotExist:
            messages.error(request=request, message="The record does not exist or has already been deleted.")
            return redirect("all-students")

# Student delete view here.
class StudentDeleteView(LoginRequiredMixin, View):
    """
    A class-based view to handle deletion of a Student record.

    Features:
    - Requires user authentication (via LoginRequiredMixin).
    - Checks whether the user has permission to delete students.
    - On GET: Shows a confirmation page for deletion.
    - On POST: Deletes the student and redirects to the list view.
    - Handles cases where the student record does not exist.
    """

    # URL to redirect unauthenticated users to the login page.
    login_url = reverse_lazy("login")

    # Shared dictionary for passing data to the template.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handles GET request to show delete confirmation page.

        - Checks delete permission.
        - Retrieves the student instance by primary key (`pk`).
        - Renders confirmation template if student exists.
        - Redirects with an error if student does not exist.
        """
        try:
            # Check if the user has permission to delete students.
            if not request.user.has_perm("student.delete_student"):
                messages.error(request=request, message="You do not have permission to access this page.")
                return redirect("dashboard")

            # Set page title for the confirmation dialog.
            self.context["title"] = "Delete Student Confirmation"

            # Retrieve the student to be deleted using the primary key from URL.
            self.context["student"] = Student.objects.get(pk=kwargs.get("pk"))

            # Render the delete confirmation page with student info.
            return render(request, "student/delete-student-confirmation.html", self.context)

        # If the student doesn't exist, handle it gracefully.
        except Student.DoesNotExist:
            messages.error(request=request, message="The record does not exist or has already been deleted.")
            return redirect("all-students")

    def post(self, request, *args, **kwargs):
        """
        Handles POST request to perform the deletion.

        - Retrieves the student by primary key (`pk`).
        - Deletes the student instance.
        - Displays a success or error message based on result.
        - If student does not exist, handles gracefully.
        """
        try:
            # Retrieve the student record to delete.
            self.context["student"] = Student.objects.get(pk=kwargs.get("pk"))

            # Perform the deletion. `.delete()` returns a tuple (number of deleted objects, details).
            deleted_count, deleted_object = self.context["student"].delete()

            # If deletion was successful, show a success message.
            if deleted_count > 0:
                messages.success(request=request, message="The record has been deleted successfully.")
            else:
                # Rare case: delete didn't work even though object was found.
                messages.error(request=request, message="The record has not been deleted. Try again.")

        # If the student record does not exist, show appropriate error.
        except Student.DoesNotExist:
            messages.error(request=request, message="The record does not exist or has already been deleted.")

        # Redirect to the all-students list page after deletion attempt.
        return redirect("all-students")