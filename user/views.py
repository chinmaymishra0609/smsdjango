from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import CustomRegistrationForm, CustomLoginForm, CustomChangePasswordForm, CustomSetPasswordForm
from django.contrib.auth import login, logout, update_session_auth_hash

# User registration view here.
class UserRegistrationView(View):
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("add-student")

        self.context["title"] = "Registeration"
        self.context["form"] = CustomRegistrationForm(label_suffix="")
        return render(request=request, template_name="user/registration.html", context=self.context)

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Registeration"
        self.context["form"] = CustomRegistrationForm(request.POST, label_suffix="")

        if self.context["form"].is_valid():
            user = self.context["form"].save()

            if user:
                messages.success(request, "Your registration has been done successfully.")
                return redirect("login")
            else:
                messages.error(request, "Your registration has not been done. Try again.")

        return render(request=request, template_name="user/registration.html", context=self.context)

# User login view here.
class UserLoginView(View):
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("add-student")

        self.context["title"] = "Login"
        self.context["form"] = CustomLoginForm(label_suffix="")
        return render(request=request, template_name="user/login.html", context=self.context)

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Login"
        self.context["form"] = CustomLoginForm(request=request, data=request.POST, label_suffix="")

        if self.context["form"].is_valid():
            login(request=request, user=self.context["form"].get_user())
            messages.success(request, "You have successfully logged in.")
            return redirect("add-student")
        else:
            messages.error(request, "Invalid credential. Try again.")

        return render(request=request, template_name="user/login.html", context=self.context)

# User change password view here.
class UserChangePasswordView(View):
    context = {}

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        self.context["title"] = "Change Password"
        self.context["form"] = CustomChangePasswordForm(label_suffix="", user=request.user)
        return render(request=request, template_name="user/change-password.html", context=self.context)

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Change Password"
        self.context["form"] = CustomChangePasswordForm(label_suffix="", user=request.user, data=request.POST)

        if self.context["form"].is_valid():
            user = self.context["form"].save()

            if user:
                update_session_auth_hash(request, self.context["form"].user)
                messages.success(request, "Your password has been changed successfully.")
                return redirect("add-student")
            else:
                messages.error(request, "Your password has not been changed. Try again.")

        return render(request=request, template_name="user/change-password.html", context=self.context)

# User set password view here.
class UserSetPasswordView(View):
    context = {}

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        self.context["title"] = "Set Password"
        self.context["form"] = CustomSetPasswordForm(label_suffix="", user=request.user)
        return render(request=request, template_name="user/set-password.html", context=self.context)

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Set Password"
        self.context["form"] = CustomSetPasswordForm(label_suffix="", user=request.user, data=request.POST)

        if self.context["form"].is_valid():
            user = self.context["form"].save()

            if user:
                update_session_auth_hash(request, self.context["form"].user)
                messages.success(request, "Your password has been changed successfully.")
                return redirect("add-student")
            else:
                messages.error(request, "Your password has not been changed. Try again.")

        return render(request=request, template_name="user/set-password.html", context=self.context)

# User logout view here.
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        logout(request=request)

        if not request.user.is_authenticated:
            messages.success(request, "You have successfully logged out.")
            return redirect("login")
        else:
            messages.error(request, "You have not logged out. Try again.")
            return redirect("add-student")