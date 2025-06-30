# Import functions to render templates and redirect users.
from django.shortcuts import render, redirect

# Import utility to lazily reverse URL names into actual URLs.
from django.urls import reverse_lazy

# Import messaging framework to send one-time alerts to users.
from django.contrib import messages

# Import custom forms for user-related functionalities like register, login, profile update, password management.
from .forms import (
    CustomUserCreateForm,            # Form to create a new user.
    CustomUserUpdateForm,            # Form to update an existing user.
    CustomUserLoginForm,             # Form for user login.
    CustomUserChangePasswordForm,    # Form to change password when old password is known.
    CustomUserSetPasswordForm,       # Form to set password without old password (e.g., reset).
    CustomUpdateAdminProfileForm,    # Form to update admin profile.
    CustomUpdateUserProfileForm,     # Form to update regular user profile.
    CustomPasswordResetForm          # Form to request a password reset.
)

# Import Django auth functions for logging users in/out and keeping sessions valid.
from django.contrib.auth import login, logout, update_session_auth_hash

# Import built-in Django views for handling password reset flow.
from django.contrib.auth.views import (
    PasswordResetView,              # View to request a password reset.
    PasswordResetDoneView,          # View shown after password reset request is submitted.
    PasswordResetCompleteView       # View shown after password reset process is completed.
)

# Import utility to decode a base64-encoded string used in password reset URLs.
from django.utils.http import urlsafe_base64_decode

# Import built-in User model.
from django.contrib.auth.models import User

# Import Django’s default token generator for password reset and email verification.
from django.contrib.auth.tokens import default_token_generator

# Import mixin to restrict access to views to authenticated users only.
from django.contrib.auth.mixins import LoginRequiredMixin

# Import pagination classes to handle dividing querysets into pages.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Import base class for creating class-based views.
from django.views import View

# Import Student model from the student app (likely used for listing or managing student data).
from student.models import Student

# Import a custom view to handle sending email (likely a wrapper for Django’s email sending).
from core.views import CustomSendMail

# User login view here.
class UserLoginView(View):
    """
    View to handle user login functionality using GET and POST requests.
    
    - GET: Renders the login form if the user is not authenticated.
    - POST: Authenticates the user and logs them in if credentials are valid.
    """

    # Define a class-level dictionary to store context data for the template.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handle GET request.
        If user is already authenticated, redirect to dashboard.
        Otherwise, render the login page with the login form.
        """

        # Check if user is already logged in.
        if request.user.is_authenticated:
            # Redirect authenticated users directly to the dashboard.
            return redirect("dashboard")

        # Set the title for the login page.
        self.context["title"] = "Login"

        # Initialize the login form (empty) and pass it to context.
        self.context["form"] = CustomUserLoginForm(label_suffix="")

        # Render the login page with form.
        return render(request=request, template_name="user/login.html", context=self.context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request.
        Validates login form and logs in the user if credentials are correct.
        Displays appropriate success or error message.
        """

        # Set the title again in case of failed form submission.
        self.context["title"] = "Login"

        # Initialize the login form with POST data.
        self.context["form"] = CustomUserLoginForm(request=request, data=request.POST, label_suffix="")

        # Validate the login form.
        if self.context["form"].is_valid():
            # If form is valid, log the user in using the authenticated user from the form.
            login(request=request, user=self.context["form"].get_user())

            # Show success message to user.
            messages.success(request=request, message="You have successfully logged in.")

            # Redirect to dashboard upon successful login.
            return redirect("dashboard")
        else:
            # If form is invalid, show error message.
            messages.error(request=request, message="Invalid credential. Try again.")

        # Re-render the login form with error messages.
        return render(request=request, template_name="user/login.html", context=self.context)

# User password reset view here.
class UserPasswordResetView(PasswordResetView):
    """
    Custom view to handle password reset request.
    Extends Django's built-in PasswordResetView to customize the templates,
    add custom form, and provide user feedback messages.

    - GET: Renders the password reset form for non-authenticated users.
    - POST: Validates the form, sends reset email, and handles success/error messages.
    """

    # Class-level context dictionary used to pass data to templates.
    context = {}

    # HTML email template for the password reset email (for clients that support HTML).
    html_email_template_name = "user/password-reset-email.html"

    # Plain text fallback email template (used by Django if HTML email fails or not supported)
    email_template_name = "user/password-reset-email.html"

    # Template for the subject of the reset password email.
    subject_template_name = "user/password-reset-subject.txt"

    # URL to redirect to after successful form submission.
    success_url = reverse_lazy("password-reset-done")

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Renders the password reset form if the user is not authenticated.
        Redirects to dashboard if already logged in.
        """

        # If the user is already logged in, redirect to dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Set the page title in the context.
        self.context["title"] = "Reset Password"

        # Instantiate an empty custom password reset form.
        self.context["form"] = CustomPasswordResetForm(label_suffix="")

        # Render the password reset template with the context.
        return render(request=request, template_name="user/password-reset.html", context=self.context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        Validates the form and sends a password reset email if the email is registered.
        Adds success or error messages depending on the outcome.
        """

        # Set the page title again for context during re-rendering.
        self.context["title"] = "Reset Password"

        # Bind POST data to the custom password reset form.
        self.context["form"] = CustomPasswordResetForm(request.POST, label_suffix="")

        # Check if the form is valid (i.e., email is registered, etc.).
        if self.context["form"].is_valid():
            # Call the parent class's post method to handle sending the email.
            response = super().post(request, *args, **kwargs)

            # If the parent class redirects (302), assume success.
            if response.status_code == 302:
                messages.success(request=request, message="The password reset link has been sent.")
            else:
                # In case the response is not a redirect, assume something went wrong.
                messages.error(request=request, message="The password reset link has not been sent. Try again.")

            # Redirect to the password reset done page regardless of outcome.
            return redirect("password-reset-done")

        # If form is invalid, re-render the reset form with validation errors.
        return render(request=request, template_name="user/password-reset.html", context=self.context)

# User password reset done view here.
class UserPasswordResetDoneView(PasswordResetDoneView):
    """
    Custom view that handles displaying the 'Password Reset Link Sent' confirmation page.
    This view is shown after the user submits a valid password reset form.

    - GET: Renders a success message that the password reset link has been sent.
      If the user is already authenticated, they are redirected to the dashboard.
    """

    # Class-level dictionary to store context data for rendering the template.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Renders the password reset done confirmation page with a custom title.
        Redirects authenticated users to the dashboard.
        """

        # If the user is already logged in, redirect them to the dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Set the page title to display in the template.
        self.context["title"] = "Password Reset Link Sent"

        # Render the 'password reset done' page with the given context and template.
        return render(request=request, template_name="user/password-reset-done.html", context=self.context)

# User password reset confirm view here.
class UserPasswordResetConfirmView(View):
    """
    Custom view to handle the confirmation of a password reset.
    This view is accessed when a user clicks the password reset link sent via email.

    - GET: Validates the UID and token in the URL, displays a form to set a new password.
    - POST: Submits the new password, saves it if valid, and sends a confirmation email.
    """

    # Shared context dictionary for storing template variables.
    context = {}

    def get_user(self, uidb64):
        """
        Decode the base64-encoded UID and return the associated user object.
        Returns None if decoding fails or user does not exist.
        """
        try:
            # Decode the UID from base64 format.
            uid = urlsafe_base64_decode(uidb64).decode()

            # Fetch the user by primary key.
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            # Return None if decoding fails or user is not found.
            user = None

        # Return the resolved user or None.
        return user

    def get(self, request, *args, **kwargs):
        """
        Handle GET request.
        Validates the reset link (token and user).
        If valid, displays the form to set a new password.
        """

        # Redirect authenticated users to dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Get user from UID in the URL.
        user = self.get_user(kwargs.get("uidb64"))

        # Check if user exists and token is valid.
        if user is not None and default_token_generator.check_token(user, kwargs.get("token")):
            # Set flag that link is valid.
            self.context["validlink"] = True

            # Set the title of the page.
            self.context["title"] = "New Password"

            # Initialize the password reset form for this user.
            self.context["form"] = CustomUserSetPasswordForm(label_suffix="", user=user)

            # Render the password reset confirm template.
            return render(request=request, template_name="user/password-reset-confirm.html", context=self.context)
        else:
            # If token is invalid or expired, show an error message.
            messages.error(request=request, message="The password reset link is invalid or expired.")
            return redirect("password-reset")

    def post(self, request, *args, **kwargs):
        """
        Handle POST request.
        Validates and saves the new password if token and UID are correct.
        Sends a confirmation email on success.
        """

        # Resolve the user from the encoded UID.
        user = self.get_user(kwargs.get("uidb64"))

        # Check if the user exists and the token is valid.
        if user is not None and default_token_generator.check_token(user, kwargs.get("token")):
            # Set the title for the template.
            self.context["title"] = "New Password"

            # Bind POST data to the password reset form.
            self.context["form"] = CustomUserSetPasswordForm(label_suffix="", data=request.POST, user=user)

            # Validate the form.
            if self.context["form"].is_valid():
                # Save the new password.
                result = self.context["form"].save()

                if result:
                    # Initialize custom email sender.
                    custom_send_mail = CustomSendMail()

                    # Send confirmation email to the user.
                    is_mail_send = custom_send_mail.send_mail(
                        request=request,
                        subject="Your Password Changed",
                        template_name="user/password-change-email.html",
                        template_params={"user": user, "title": "Your Password Changed"},
                        recipient_list=[user.email],
                    )

                    # Show appropriate message based on email sending result.
                    if is_mail_send:
                        messages.success(request=request, message="The password has been reset successfully.")
                    else:
                        messages.error(request=request, message="The password has been reset but email not sent.")

                    # Redirect to password reset complete view.
                    return redirect("password-reset-complete")
                else:
                    # In case form.save() returned False (custom logic), show error.
                    messages.error(request=request, message="The password has not been reset. Try again.")

                # Redirect to login if result was False.
                return redirect("login")
        else:
            # If the token or user is invalid, show error and redirect.
            messages.error(request=request, message="The password reset link is invalid or expired.")
            return redirect("password-reset")

        # If form is invalid, re-render the form with validation errors.
        return render(request=request, template_name="user/password-reset-confirm.html", context=self.context)

# User password reset complete view here.
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Custom view that displays the confirmation page after a user has successfully reset their password.
    Extends Django's built-in PasswordResetCompleteView.

    - GET: Renders a 'Password Reset Complete' page to inform the user that the process is done.
           If the user is already authenticated, they are redirected to the dashboard.
    """

    # Class-level dictionary to store context data for the template.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        If the user is already authenticated, redirect them to the dashboard.
        Otherwise, render the password reset complete confirmation page.
        """

        # If the user is logged in, redirect to the dashboard as they don't need to see this page.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Set the page title to display in the template.
        self.context["title"] = "New Password"

        # Render the password reset complete page with the context.
        return render(request=request, template_name="user/password-reset-complete.html", context=self.context)

# Create Dashboard view here.
class UserDashboardView(LoginRequiredMixin, View):
    """
    Custom view to display the user dashboard.
    Inherits from Django's View and uses LoginRequiredMixin to restrict access to authenticated users only.
    
    - GET: Shows statistics of active/inactive admin users, staff, and total students.
    """

    # URL to redirect unauthenticated users if they try to access the dashboard.
    login_url = reverse_lazy("login")

    # Dictionary used to store and pass data to the template.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Only accessible by authenticated users.
        Fetches user and student statistics and renders the dashboard template.
        """

        # Set the title for the dashboard page.
        self.context["title"] = "Dashboard"

        # Count active admin users (superuser + staff + active).
        self.context["active_admin_users"] = User.objects.filter(is_superuser=True, is_staff=True, is_active=True).count()

        # Count inactive admin users (superuser + staff + not active).
        self.context["inactive_admin_users"] = User.objects.filter(is_superuser=True, is_staff=True, is_active=False).count()

        # Count active staff users (not superuser + staff + active).
        self.context["active_staff_users"] = User.objects.filter(is_superuser=False, is_staff=True, is_active=True).count()

        # Count inactive staff users (not superuser + staff + not active).
        self.context["inactive_staff_users"] = User.objects.filter(is_superuser=False, is_staff=True, is_active=False).count()

        # Count all students (assuming all students are active).
        self.context["active_students"] = Student.objects.all().count()

        # Render the dashboard template with all the context data.
        return render(request=request, template_name="user/dashboard.html", context=self.context)

# User create view here.
class UserCreateView(LoginRequiredMixin, View):
    """
    Custom view to handle creation of new user accounts.
    Only accessible to users with 'auth.add_user' permission.
    Sends a welcome email to the new user upon successful creation.

    - GET: Renders the user creation form.
    - POST: Validates and saves the form, then sends a welcome email.
    """

    # URL to redirect to if the user is not logged in.
    login_url = reverse_lazy("login")

    # Dictionary to store context data passed to the template.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Renders the 'Add User' form if the user has permission.
        Otherwise, redirects to the dashboard with an error message.
        """

        # Check if the user has permission to add a user.
        if not request.user.has_perm("auth.add_user"):
            # Show error and redirect to dashboard if permission is missing.
            messages.error(request=request, message="You do not have permission to access this page.")
            return redirect("dashboard")

        # Set page title.
        self.context["title"] = "Add User"

        # Create a blank user creation form.
        self.context["form"] = CustomUserCreateForm(label_suffix="")

        # Render the add-user template with the form.
        return render(request=request, template_name="user/add-update-user.html", context=self.context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        Processes form data to create a new user and sends them a welcome email.
        Displays appropriate success/error messages.
        """

        # Set page title.
        self.context["title"] = "Add User"

        # Bind submitted data to the form.
        self.context["form"] = CustomUserCreateForm(request.POST, label_suffix="")

        # Validate the form.
        if self.context["form"].is_valid():
            # Save the user (commit=True by default).
            user = self.context["form"].save()

            # Check if user was successfully created.
            if user:
                # Create instance of custom email sender.
                custom_send_mail = CustomSendMail()

                # Attempt to send welcome email.
                is_mail_send = custom_send_mail.send_mail(
                    request=request,
                    subject="Welcome to SMS",
                    recipient_list=[user.email],
                    template_name="user/welcome-email.html",
                    template_params={
                        "title": "Welcome to SMS",
                        "user": user,
                        "password": self.context["form"].cleaned_data.get("password1"), # Raw password to show in email.
                    }
                )

                # If email sent successfully, show success message.
                if is_mail_send:
                    messages.success(request=request, message="The record has been saved successfully.")
                else:
                    # If email sending fails, notify user but acknowledge save.
                    messages.error(request=request, message="The record has been saved but email not sent.")

                # Redirect to the same add-user form (useful for adding multiple users).
                return redirect("add-user")
            else:
                # If user creation failed (unexpectedly), show error.
                messages.error(request=request, message="The password has not been reset. Try again.")

        # If form is invalid or user creation failed, re-render the form with errors.
        return render(request=request, template_name="user/add-update-user.html", context=self.context)

# User update view here.
class UserUpdateView(LoginRequiredMixin, View):
    """
    Custom view to update an existing user's information.
    Only accessible to users with 'auth.change_user' permission.

    - GET: Renders a pre-filled form with user data for editing.
    - POST: Validates and updates the user record, then provides feedback messages.
    """

    # URL to redirect to if the user is not authenticated.
    login_url = reverse_lazy("login")

    # Shared context dictionary for passing data to templates.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Fetches the user by primary key and displays the update form.
        Redirects if permission is missing or user does not exist.
        """

        try:
            # Check if the current user has permission to update users.
            if not request.user.has_perm("auth.change_user"):
                # Show error message and redirect to dashboard if no permission.
                messages.error(request=request, message="You do not have permission to access this page.")
                return redirect("dashboard")

            # Get the user to be edited using primary key from URL.
            user = User.objects.get(pk=kwargs.get("pk"))

            # Set page title.
            self.context["title"] = "Update User"

            # Populate the form with existing user data (edit mode).
            self.context["form"] = CustomUserUpdateForm(instance=user, label_suffix="")

            # Render the add/update user form with existing data.
            return render(request=request, template_name="user/add-update-user.html", context=self.context)
        except User.DoesNotExist:
            # If the user does not exist, show an error and redirect.
            messages.error(request=request, message="The record does not exist or has already been deleted.")
            return redirect("all-users")

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        Validates and updates the user information in the database.
        """

        # Set the page title again for the template context.
        self.context["title"] = "Update User"

        # Fetch the user object to update.
        user = User.objects.get(pk=kwargs.get("pk"))

        # Bind submitted data to the form with the user instance (edit mode).
        self.context["form"] = CustomUserUpdateForm(request.POST, instance=user, label_suffix="")

        # Validate the form.
        if self.context["form"].is_valid():
            # Save the updated user data.
            user = self.context["form"].save()

            # Check if update was successful.
            if user:
                messages.success(request=request, message="The record has been updated successfully.")
            else:
                messages.error(request=request, message="The record has not been updated. Try again.")

            # Redirect to the same update page (allows user to confirm or keep editing).
            return redirect("update-user", user.id)

        # If form is invalid, re-render the form with error messages.
        return render(request=request, template_name="user/add-update-user.html", context=self.context)

# User update profile view here.
class UserUpdateProfileView(LoginRequiredMixin, View):
    """
    Custom view that allows users to update their profile.
    Superusers and users with 'auth.change_user' permission can update any profile,
    while regular users can only update their own.

    - GET: Displays the profile form pre-filled with user data.
    - POST: Processes the profile update and provides feedback.
    """

    # Redirect to login if unauthenticated.
    login_url = reverse_lazy("login")

    # Dictionary to hold context variables for rendering the template.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Displays the user profile update form based on user type (admin or regular).
        Ensures proper permission or ownership before allowing access.
        """

        try:
            # Permission check:
            # Allow only if the user has 'change_user' permission OR is editing their own profile.
            if not request.user.has_perm("auth.change_user") and request.user.id != kwargs.get("pk"):
                messages.error(request=request, message="You do not have permission to access this page.")
                return redirect("dashboard")

            # Set the title for the page.
            self.context["title"] = "Update Profile"

            # Fetch the user object using primary key from URL.
            user = User.objects.get(pk=kwargs.get("pk"))

            # Check if current user is a superuser.
            if request.user.is_superuser == True:
                # Use admin-specific form for updating profile.
                self.context["form"] = CustomUpdateAdminProfileForm(instance=user, label_suffix="")
            else:
                # Use regular user-specific profile form.
                self.context["form"] = CustomUpdateUserProfileForm(instance=user, label_suffix="")

            # Render the update profile page with the form.
            return render(request=request, template_name="user/update-profile.html", context=self.context)
        except User.DoesNotExist:
            # Handle case where user record is missing.
            messages.error(request=request, message="The record does not exist or has already been deleted.")
            return redirect("all-users")

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        Validates and updates the user's profile based on their user type.
        Provides success or error feedback.
        """

        # Set the page title again for consistency.
        self.context["title"] = "Update Profile"

        # Retrieve the user instance from the URL primary key.
        user = User.objects.get(pk=kwargs.get("pk"))

        # Use appropriate form class based on current user's superuser status.
        if request.user.is_superuser == True:
            self.context["form"] = CustomUpdateAdminProfileForm(request.POST, instance=user, label_suffix="")
        else:
            self.context["form"] = CustomUpdateUserProfileForm(request.POST, instance=user, label_suffix="")

        # Check if the submitted form is valid.
        if self.context["form"].is_valid():
            # Save the changes to the user profile.
            user = self.context["form"].save()

            if user:
                # Show success message.
                messages.success(request=request, message="Your profile has been updated successfully.")
            else:
                # Show error message if save failed.
                messages.error(request=request, message="Your profile has not been updated. Try again.")

            # Redirect to the same update profile page.
            return redirect("update-profile", user.id)

        # If form is invalid, re-render the page with errors.
        return render(request=request, template_name="user/update-profile.html", context=self.context)

# User list view here.
class UserListView(LoginRequiredMixin, View):
    """
    Custom view to list all user accounts in a paginated table.
    Access is restricted to users with any of the following permissions:
    - auth.view_user
    - auth.change_user
    - auth.delete_user

    Pagination is customizable via a 'per-page' query parameter.
    """

    # Redirect URL for unauthenticated users.
    login_url = reverse_lazy("login")

    # Dictionary to store context variables for template rendering.
    context = {}

    def get(self, request):
        """
        Handle GET requests.
        Validates user permissions, paginates user list, and renders the user list view.
        """

        # Check if the user has at least one required permission to view this page.
        if not request.user.has_perm("auth.view_user") and \
           not request.user.has_perm("auth.change_user") and \
           not request.user.has_perm("auth.delete_user"):
            # If user lacks all permissions, deny access and redirect to dashboard.
            messages.error(request=request, message="You do not have permission to access this page.")
            return redirect("dashboard")

        # Get the number of items to display per page from query params, default is "10".
        per_page = request.GET.get("per-page", "10")

        # Validate and sanitize the `per_page` input.
        if not per_page.isdigit() or int(per_page) <= 0:
            # If invalid (non-numeric or less than 1), default to 10.
            per_page = 10
        else:
            # Convert to integer and limit maximum page size to 100.
            per_page = min(int(per_page), 100)

        # Fetch all users from the database, ordered by primary key.
        user_lists = User.objects.all().order_by("id")

        # Initialize Django's paginator with user list and per_page count.
        paginator = Paginator(user_lists, per_page)

        # Get the current page number from query parameters.
        current_page_number = request.GET.get("page")

        try:
            # Try to fetch the requested page.
            users = paginator.page(current_page_number)
        except PageNotAnInteger:
            # If page is not an integer, show the first page.
            users = paginator.page(1)
        except EmptyPage:
            # If page number is out of range, show the last page.
            users = paginator.page(paginator.num_pages)

        # Add paginated users to context for template rendering.
        self.context["users"] = users

        # Add per_page value to context for use in pagination controls.
        self.context["per_page"] = per_page

        # Set the page title.
        self.context["title"] = "All Users"

        # Render the user listing page with context data.
        return render(request, "user/all-users.html", self.context)

# User change password view here.
class UserChangePasswordView(LoginRequiredMixin, View):
    """
    View to allow authenticated users to change their password.
    Requires user to be logged in (via LoginRequiredMixin).

    - GET: Displays the password change form.
    - POST: Validates and updates the password, and keeps the user logged in after update.
    """

    # URL to redirect unauthenticated users.
    login_url = reverse_lazy("login")

    # Dictionary to store data passed to the template.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Render the password change form with the currently authenticated user.
        """

        # Set the page title.
        self.context["title"] = "Change Password"

        # Initialize the custom password change form with current user instance.
        self.context["form"] = CustomUserChangePasswordForm(label_suffix="", user=request.user)

        # Render the form in the 'change-password.html' template.
        return render(request=request, template_name="user/change-password.html", context=self.context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        Validates the form, changes the user's password, and updates the session auth hash to keep the user logged in.
        """

        # Set the page title again for template context.
        self.context["title"] = "Change Password"

        # Bind submitted data to the form for validation.
        self.context["form"] = CustomUserChangePasswordForm(label_suffix="", user=request.user, data=request.POST)

        # Check if the form is valid.
        if self.context["form"].is_valid():
            # Save the new password for the user.
            user = self.context["form"].save()

            if user:
                # Update the session with the new password to prevent logout.
                update_session_auth_hash(request, self.context["form"].user)

                # Display success message.
                messages.success(request=request, message="Your password has been changed successfully.")
            else:
                # Display error if password update failed (rare case).
                messages.error(request=request, message="Your password has not been changed. Try again.")

            # Redirect to a post-password-change page (example: change-password)
            return redirect("change-password")

        # If form is invalid, re-render the page with error messages
        return render(request=request, template_name="user/change-password.html", context=self.context)

# User set password view here.
class UserSetPasswordView(LoginRequiredMixin, View):
    """
    View to allow authenticated users to set a new password (without entering the old one).
    Useful in cases such as:
    - First-time password setup
    - Password reset via token
    - External login where password was not previously set

    - GET: Renders the set password form.
    - POST: Validates and saves the new password, keeping the user logged in.
    """

    # If the user is not authenticated, they will be redirected to the login page.
    login_url = reverse_lazy("login")

    # Context dictionary to pass data to the template.
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Renders the set-password form for the currently logged-in user.
        """

        # Set the page title.
        self.context["title"] = "Set Password"

        # Initialize the set password form for the current user (no old password required).
        self.context["form"] = CustomUserSetPasswordForm(label_suffix="", user=request.user)

        # Render the form using the template 'set-password.html'.
        return render(request=request, template_name="user/set-password.html", context=self.context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.
        Processes the set-password form submission.
        Validates and saves the new password, then keeps the user logged in.
        """

        # Set the page title again for the post request.
        self.context["title"] = "Set Password"

        # Bind POST data to the set password form for the current user.
        self.context["form"] = CustomUserSetPasswordForm(label_suffix="", user=request.user, data=request.POST)

        # Check if the form data is valid.
        if self.context["form"].is_valid():
            # Save the new password to the user model.
            user = self.context["form"].save()

            if user:
                # Update session auth hash to prevent logout after password change.
                update_session_auth_hash(request, self.context["form"].user)

                # Show success message.
                messages.success(request=request, message="Your password has been changed successfully.")
            else:
                # Show error message if password update failed.
                messages.error(request=request, message="Your password has not been changed. Try again.")

            # Redirect user to a new page after success (e.g., set-password page)
            return redirect("set-password")

        # If form is invalid, render the same form with errors.
        return render(request=request, template_name="user/set-password.html", context=self.context)

# User logout view here.
class UserLogoutView(LoginRequiredMixin, View):
    """
    Handles user logout for authenticated users.
    Ensures that only logged-in users can access this view.
    Logs the user out and provides appropriate feedback using messages framework.

    - GET: Logs the user out and redirects to login page.
    """

    # Redirect URL if the user is not logged in.
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        Logs out the user and shows success or error message accordingly.
        """

        # Perform the logout action using Django's built-in logout method.
        logout(request=request)

        # After logout, check if the user is truly unauthenticated.
        if not request.user.is_authenticated:
            # If successfully logged out, show a success message.
            messages.success(request=request, message="You have successfully logged out.")

            # Redirect to the login page.
            return redirect("login")
        else:
            # If logout failed for some reason, show an error message.
            messages.error(request=request, message="You have not logged out. Try again.")

            # Redirect to another page (in this case, 'dashboard')
            return redirect("dashboard")