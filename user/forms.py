from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm

# Create custom user change form here.
class CustomUserChangeForm(UserChangeForm):
    STATUS = [("", "---------"), (0, "No"), (1, "Yes")]

    username         = forms.CharField(label="Username", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name       = forms.CharField(label="First Name", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name        = forms.CharField(label="Last Name", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    email            = forms.CharField(label="Email", required=True, widget=forms.EmailInput(attrs={"class":"form-control"}))
    is_superuser     = forms.ChoiceField(label="Superuser Status", required=True, choices=STATUS, widget=forms.Select(attrs={"class":"form-select"}))
    is_staff         = forms.ChoiceField(label="Staff Status", required=True, choices=STATUS, widget=forms.Select(attrs={"class":"form-select"}))
    is_active        = forms.ChoiceField(label="Active Status", required=True, choices=STATUS, widget=forms.Select(attrs={"class":"form-select"}))
    groups           = forms.ModelMultipleChoiceField(label="Groups", required=False, queryset=Group.objects.all(), widget=forms.SelectMultiple(attrs={"class":"form-select", "type":"datetime-local", "readonly":True}))
    user_permissions = forms.ModelMultipleChoiceField(label="Permissions", required=False, queryset=Permission.objects.all(), widget=forms.SelectMultiple(attrs={"class":"form-select", "type":"datetime-local", "readonly":True}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_superuser", "is_staff", "is_active", "groups", "user_permissions"]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This username is already exist.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already exist.")
        return email

    def clean(self):
        cleaned_data = super().clean()

        groups = self.cleaned_data.get("groups")
        user_permissions = self.cleaned_data.get("user_permissions")

        if not groups and not user_permissions:
            self.add_error(field="groups", error="Either select any permissions.")
            self.add_error(field="user_permissions", error="Either select any groups.")

        for field in ["is_superuser", "is_staff", "is_active"]:
            value = self.cleaned_data.get(field)
            if value is not None:
                if value not in ("0", "1"):
                    self.add_error(field=field, error="Invalid status selected.")
                else:
                    cleaned_data[field] = value == "1"

        return cleaned_data

# Create custom user create form here.
class CustomUserCreateForm(CustomUserChangeForm, UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta(CustomUserChangeForm.Meta):
        fields = CustomUserChangeForm._meta.fields + ["password1", "password2"]

# Create custom user update form here.
class CustomUserUpdateForm(CustomUserChangeForm):
    date_joined = forms.DateTimeField(label="Date Joined", required=False, widget=forms.DateTimeInput(attrs={"class":"form-select", "type":"datetime-local", "disabled":True}))
    last_login  = forms.DateTimeField(label="Last Login", required=False, widget=forms.DateTimeInput(attrs={"class":"form-select", "type":"datetime-local", "disabled":True}))

    class Meta(CustomUserChangeForm.Meta):
        fields = CustomUserChangeForm._meta.fields + ["date_joined", "last_login"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ["is_superuser", "is_staff", "is_active"]:
            value = getattr(self.instance, field, None)

            if value is not None:
                self.initial[field] = "1" if value else "0"

# Create custom update admin profile form here.
class CustomUpdateAdminProfileForm(CustomUserChangeForm):
    date_joined = forms.DateTimeField(label="Date Joined", required=False, widget=forms.DateTimeInput(attrs={"class":"form-select", "type":"datetime-local", "disabled":True}))
    last_login  = forms.DateTimeField(label="Last Login", required=False, widget=forms.DateTimeInput(attrs={"class":"form-select", "type":"datetime-local", "disabled":True}))

    class Meta:
        model = User
        fields = "__all__"

# Create custom update user profile form here.
class CustomUpdateUserProfileForm(CustomUserChangeForm):
    date_joined      = forms.DateTimeField(label="Date Joined", required=False, widget=forms.DateTimeInput(attrs={"class":"form-select", "type":"datetime-local", "disabled":True}))
    last_login       = forms.DateTimeField(label="Last Login", required=False, widget=forms.DateTimeInput(attrs={"class":"form-select", "type":"datetime-local", "disabled":True}))
    groups           = None
    user_permissions = None

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "date_joined", "last_login"]

# Create custom password reset form here.
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={"class":"form-control"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not User.objects.filter(email=email).exists():
            raise ValidationError("Email address it not exist.")
        return email

# Create custom user login form here.
class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

# Create custom user set password form here.
class CustomUserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

# Create custom user change password form here.
class CustomUserChangePasswordForm(PasswordChangeForm):
    old_password  = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))