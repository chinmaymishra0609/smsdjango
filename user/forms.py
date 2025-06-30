# Importing the `forms` module from Django to create and handle HTML forms.
from django import forms

# Importing Django's built-in `User`, `Group`, and `Permission` models used for authentication and authorization.
from django.contrib.auth.models import User, Group, Permission

# Importing Django's `ValidationError` class to raise validation errors during form processing.
from django.core.exceptions import ValidationError

# Importing several built-in authentication forms from Django's `auth.forms` module:
# - `UserCreationForm`: For creating a new user with username and password.
# - `AuthenticationForm`: For authenticating (login) a user.
# - `UserChangeForm`: For updating a user’s information.
# - `PasswordChangeForm`: For allowing users to change their password while logged in.
# - `SetPasswordForm`: For setting a new password without old password (typically during reset).
# - `PasswordResetForm`: For initiating password reset via email.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm

# Create custom user change form here.
# This form is intended for admin or backend users to update an existing User model instance
# with additional validations and customized widget styling.
# Inheriting from Django's built-in UserChangeForm to modify the default behavior.
class CustomUserChangeForm(UserChangeForm):
    # Defining choices for status-related fields where 0 means No (False) and 1 means Yes (True).
    STATUS = [("", "---------"), (0, "No"), (1, "Yes")]

    # Defining form fields with labels, required validation, and Bootstrap CSS classes for styling.
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    first_name = forms.CharField(
        label="First Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        label="Last Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.CharField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    is_superuser = forms.ChoiceField(
        label="Superuser Status",
        required=True,
        choices=STATUS,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    is_staff = forms.ChoiceField(
        label="Staff Status",
        required=True,
        choices=STATUS,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    is_active = forms.ChoiceField(
        label="Active Status",
        required=True,
        choices=STATUS,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    # `groups` field allows selecting multiple groups (roles). It's not required.
    groups = forms.ModelMultipleChoiceField(
        label="Groups",
        required=False,
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )

    # `user_permissions` field allows selecting multiple specific permissions for the user.
    user_permissions = forms.ModelMultipleChoiceField(
        label="Permissions",
        required=False,
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )

    # Meta configuration to specify the model and fields used by this form.
    class Meta:
        # Binds the form to Django's built-in User model.
        model = User

        # Include the model fields in the form.
        fields = ["username", "first_name", "last_name", "email", "is_superuser", "is_staff", "is_active", "groups", "user_permissions"]

    # Custom validation for username to ensure uniqueness excluding the current instance.
    def clean_username(self):
        # Get cleaned value from submitted data.
        username = self.cleaned_data.get("username")

        # Check if any user with the same username exists, excluding the current user.
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            # Raise error if invalid.
            raise ValidationError("This username is already exist.")

        # Return cleaned value.
        return username

    # Custom validation for email to ensure uniqueness excluding the current instance.
    def clean_email(self):
        # Get cleaned value from submitted data.
        email = self.cleaned_data.get("email")

        # Check if any user with the same email exists, excluding the current user.
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            # Raise error if invalid.
            raise ValidationError("This email is already exist.")

        # Return cleaned value.
        return email

    # Overriding the clean() method to perform cross-field validation.
    def clean(self):
        # Get cleaned data from parent
        cleaned_data = super().clean()

        # Fetch group and permission values.
        groups = self.cleaned_data.get("groups")
        user_permissions = self.cleaned_data.get("user_permissions")

        # Ensure at least one of groups or user_permissions is selected.
        if not groups and not user_permissions:
            self.add_error(field="groups", error="Either select any permissions.")
            self.add_error(field="user_permissions", error="Either select any groups.")

        # Normalize status fields ("0" / "1") to Boolean values.
        for field in ["is_superuser", "is_staff", "is_active"]:
            # Get cleaned value from submitted data.
            value = self.cleaned_data.get(field)

            # Check if the value is not None.
            if value is not None:
                # If value is not 0 or 1.
                if value not in ("0", "1"):
                    # Aadd an error.
                    self.add_error(field=field, error="Invalid status selected.")
                else:
                    # Convert to Boolean: "1" -> True, "0" -> False.
                    cleaned_data[field] = value == "1"

        # Return the final cleaned data dictionary.
        return cleaned_data

# Create custom user create form here.
# This form is used to create a new user, combining custom fields from CustomUserChangeForm and the password logic from UserCreationForm.
# Define a new form for user creation by extending both CustomUserChangeForm and UserCreationForm.
# This allows reuse of field definitions from CustomUserChangeForm (e.g., username, email, status fields)
# along with password validation logic from UserCreationForm (e.g., password1/password2 match).
class CustomUserCreateForm(CustomUserChangeForm, UserCreationForm):
    # Define password1 field (the original password) using PasswordInput widget with Bootstrap styling.
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    # Define password2 field (confirmation password) to match against password1.
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    # The Meta class defines model binding and field inclusion for the form.
    class Meta(CustomUserChangeForm.Meta):
        # Inherit the fields from CustomUserChangeForm (username, email, status, etc.)
        # and add the password1 and password2 fields used for password creation.
        fields = CustomUserChangeForm._meta.fields + ["password1", "password2"]

# Create custom user update form here.
# This form is used for updating an existing user and includes read-only fields like `date_joined` and `last_login`.
# Inherit from CustomUserChangeForm to reuse all user-related fields and validation logic.
class CustomUserUpdateForm(CustomUserChangeForm):
    # Add `date_joined` field to display the user's account creation date.
    # It's not required and rendered using a DateTime input with a disabled attribute (read-only).
    date_joined = forms.DateTimeField(
        label="Date Joined",
        required=False,
        widget=forms.DateTimeInput(attrs={
            "class": "form-select",         # Bootstrap class for styling
            "type": "datetime-local",       # Render as datetime-local input
            "disabled": True                # Make the input field non-editable
        })
    )

    # Add `last_login` field to show the user's last login timestamp.
    # Also disabled to prevent editing.
    last_login = forms.DateTimeField(
        label="Last Login",
        required=False,
        widget=forms.DateTimeInput(attrs={
            "class": "form-select",         # Bootstrap class for styling
            "type": "datetime-local",       # Render as datetime-local input
            "disabled": True                # Read-only field
        })
    )

    # Define the Meta class that specifies which model and fields to include in the form.
    class Meta(CustomUserChangeForm.Meta):
        # Combine all fields from the base form (CustomUserChangeForm) and add the new read-only fields.
        fields = CustomUserChangeForm._meta.fields + ["date_joined", "last_login"]

    # Customize form initialization to populate initial values for status fields correctly.
    def __init__(self, *args, **kwargs):
        # Call the parent constructor to initialize form fields and data.
        super().__init__(*args, **kwargs)

        # For the Boolean status fields (stored as True/False), convert them to "1"/"0"
        # because form expects "1"/"0" strings due to use of ChoiceField.
        for field in ["is_superuser", "is_staff", "is_active"]:
            # Get the current value (True/False) from the user instance.
            value = getattr(self.instance, field, None)

            # If value is not None.
            if value is not None:
                # Set the initial form value as a string ("1" for True, "0" for False).
                self.initial[field] = "1" if value else "0"

# Create custom update admin profile form here.
# This form is specifically used to update the Django admin user's profile.
# It includes all fields from the built-in `User` model and displays read-only metadata fields like `date_joined` and `last_login`.
# Inherit from CustomUserChangeForm to reuse existing user-related field definitions and custom validations.
class CustomUpdateAdminProfileForm(CustomUserChangeForm):
    # Add the `date_joined` field to display when the admin account was created.
    # This field is not required and is disabled so it appears read-only in the UI.
    date_joined = forms.DateTimeField(
        label="Date Joined",                # Label shown on the form.
        required=False,                     # Field is not mandatory.
        widget=forms.DateTimeInput(attrs={
            "class": "form-select",         # Use Bootstrap class for consistent styling.
            "type": "datetime-local",       # HTML5 input type for date-time selection.
            "disabled": True                # Field is disabled (non-editable).
        })
    )

    # Add the `last_login` field to display the most recent login time of the admin.
    # Like `date_joined`, this is also read-only and not required.
    last_login = forms.DateTimeField(
        label="Last Login",                 # Label shown on the form.
        required=False,                     # Field is optional.
        widget=forms.DateTimeInput(attrs={
            "class": "form-select",         # Bootstrap class for styling.
            "type": "datetime-local",       # Render input as date-time selector.
            "disabled": True                # Make the field read-only.
        })
    )

    # Define the inner Meta class to configure model and fields.
    class Meta:
        # Bind the form to Django's built-in User model.
        model = User

        # Include all fields from the User model in the form.
        fields = "__all__"

# Create custom update user profile form here.
# This form is used by regular users to update their own profile information.
# It hides group and permission-related fields and includes read-only metadata like date_joined and last_login.
# Inherit from CustomUserChangeForm to reuse field definitions and validation logic for user profile.
class CustomUpdateUserProfileForm(CustomUserChangeForm):
    # Display the date the user joined (account created).
    # This field is disabled (read-only) and optional.
    date_joined = forms.DateTimeField(
        label="Date Joined",                # Display label.
        required=False,                     # Not required in form submission.
        widget=forms.DateTimeInput(attrs={
            "class": "form-select",         # Bootstrap class for styling.
            "type": "datetime-local",       # Render as HTML datetime-local input.
            "disabled": True                # Make it non-editable.
        })
    )

    # Display the user's last login time.
    # Also read-only and not required for submission.
    last_login = forms.DateTimeField(
        label="Last Login",                 # Display label.
        required=False,                     # Optional field.
        widget=forms.DateTimeInput(attrs={
            "class": "form-select",         # Bootstrap styling.
            "type": "datetime-local",       # Render as datetime-local input.
            "disabled": True                # Make field non-editable.
        })
    )

    # Remove the `groups` field from the form by setting it to None.
    # Regular users shouldn't assign themselves to groups.
    groups = None

    # Remove the `user_permissions` field from the form by setting it to None.
    # Regular users shouldn't have access to manage their own permissions.
    user_permissions = None

    # Inner Meta class defines model binding and which fields to include in the form.
    class Meta:
        # This form is bound to Django's built-in User model.
        model = User

        # Explicitly include only the fields that regular users should be able to view or edit.
        fields = [
            "username",       # Editable field.
            "first_name",     # Editable field.
            "last_name",      # Editable field.
            "email",          # Editable field.
            "date_joined",    # Display-only.
            "last_login"      # Display-only.
        ]

# Create custom password reset form here.
# This form is used to handle the password reset request by taking a user's email.
# It extends Django's built-in PasswordResetForm and customizes the email field and its validation.
# Inherit from Django's built-in PasswordResetForm which provides password reset functionality
class CustomPasswordResetForm(PasswordResetForm):
    # Override the default email field to apply custom styling using Bootstrap and ensure it's required.
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"
        })
    )

    # Custom validation for the email field.
    def clean_email(self):
        # Extract the email from the cleaned form data.
        email = self.cleaned_data.get("email")

        # Check if the email exists in the User model.
        if not User.objects.filter(email=email).exists():
            # Raise a validation error if the email is not associated with any user.
            raise ValidationError("Email address is does not exist.")

        # Return the validated email if it exists.
        return email

# Create custom user login form here.
# This form is used to authenticate users by asking for their username and password.
# It extends Django’s built-in AuthenticationForm and applies custom styling using Bootstrap classes.
# Inherit from Django's built-in AuthenticationForm which handles login authentication logic.
class CustomUserLoginForm(AuthenticationForm):
    # Override the username field to customize the widget.
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control"
        })
    )

    # Override the password field to use a password input widget with styling.
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"
        })
    )

# Create custom user set password form here.
# This form is used to set a new password for a user, typically after a password reset link is confirmed.
# It extends Django’s built-in SetPasswordForm and adds custom styling using Bootstrap classes.
# Inherit from Django's built-in SetPasswordForm which handles setting a new password without requiring the old one.
class CustomUserSetPasswordForm(SetPasswordForm):
    # Override the new_password1 field to set a custom label and apply Bootstrap styling.
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"
        })
    )

    # Override the new_password2 field (confirmation password) with similar styling.
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"
        })
    )

# Create custom user change password form here.
# This form is used when an authenticated user wants to change their password.
# It extends Django's built-in PasswordChangeForm and adds Bootstrap styling to each field.
# Inherit from Django's built-in PasswordChangeForm, which provides the logic for changing a password
# (requires old password and confirmation of the new password).
class CustomUserChangePasswordForm(PasswordChangeForm):
    # Define the field for the old password.
    # This field is required to verify the user's identity before allowing a password change.
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"
        })
    )

    # Define the field for the new password (first entry).
    # This is where the user enters their desired new password.
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    # Define the field to confirm the new password (second entry).
    # Ensures that the user typed the new password correctly.
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )