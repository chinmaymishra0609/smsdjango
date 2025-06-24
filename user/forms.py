from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm

# Create custom registration form here.
class CustomRegistrationForm(UserCreationForm):
    STATUS = [("", "---------"), (0, "No"), (1, "Yes")]

    username     = forms.CharField(label="Username", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name   = forms.CharField(label="First Name", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name    = forms.CharField(label="Last Name", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    email        = forms.CharField(label="Email", required=True, widget=forms.EmailInput(attrs={"class":"form-control"}))
    is_superuser = forms.ChoiceField(label="Superuser Status", required=True, choices=STATUS, widget=forms.Select(attrs={"class":"form-select"}))
    is_staff     = forms.ChoiceField(label="Staff Status", required=True, choices=STATUS, widget=forms.Select(attrs={"class":"form-select"}))
    is_active    = forms.ChoiceField(label="Active Status", required=True, choices=STATUS, widget=forms.Select(attrs={"class":"form-select"}))
    password1    = forms.CharField(label="Password", widget=forms.PasswordInput( attrs={"class":"form-control"}))
    password2    = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_superuser", "is_staff", "is_active"]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already registered.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()

        for field in ["is_superuser", "is_staff", "is_active"]:
            value = self.cleaned_data.get(field)
            if value is not None:
                if value not in ("0", "1"):
                    self.add_error(field=field, error="Invalid status selected.")
                else:
                    cleaned_data[field] = value == "1"

        return cleaned_data

# Create custom login form here.
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

# Create custom set password form here.
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

# Create custom change password form here.
class CustomChangePasswordForm(PasswordChangeForm):
    old_password  = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))