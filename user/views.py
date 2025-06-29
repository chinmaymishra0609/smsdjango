from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreateForm, CustomUserUpdateForm, CustomUserLoginForm, CustomUserChangePasswordForm, CustomUserSetPasswordForm, CustomUpdateAdminProfileForm, CustomUpdateUserProfileForm, CustomPasswordResetForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from student.models import Student
from core.views import CustomSendMail

# User login view here.
class UserLoginView(View):
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")

        self.context["title"] = "Login"
        self.context["form"] = CustomUserLoginForm(label_suffix="")
        return render(request=request, template_name="user/login.html", context=self.context)

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Login"
        self.context["form"] = CustomUserLoginForm(request=request, data=request.POST, label_suffix="")

        if self.context["form"].is_valid():
            login(request=request, user=self.context["form"].get_user())
            messages.success(request=request, message="You have successfully logged in.")
            return redirect("dashboard")
        else:
            messages.error(request=request, message="Invalid credential. Try again.")

        return render(request=request, template_name="user/login.html", context=self.context)

# User password reset view here.
class UserPasswordResetView(PasswordResetView):
    context = {}

    html_email_template_name = "user/password-reset-email.html"
    email_template_name = "user/password-reset-email.html"
    subject_template_name = "user/password-reset-subject.txt"
    success_url = reverse_lazy("password-reset-done")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")

        self.context["title"] = "Reset Password"
        self.context["form"] = CustomPasswordResetForm(label_suffix="")

        return render(request=request, template_name="user/password-reset.html", context=self.context)

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Reset Password"
        self.context["form"] = CustomPasswordResetForm(request.POST, label_suffix="")

        if self.context["form"].is_valid():
            response = super().post(request, *args, **kwargs)

            if response.status_code == 302:
                messages.success(request=request, message="The password reset link has been sent.")
            else:
                messages.error(request=request, message="The password reset link has not been sent. Try again.")

            return redirect("password-reset-done")

        return render(request=request, template_name="user/password-reset.html", context=self.context)

# User password reset done view here.
class UserPasswordResetDoneView(PasswordResetDoneView):
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")

        self.context["title"] = "Password Reset Link Sent"

        return render(request=request, template_name="user/password-reset-done.html", context=self.context)

# User password reset confirm view here.
class UserPasswordResetConfirmView(View):
    context = {}

    def get_user(self, uidb64):
        # Try to get the user.
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Return the response.
        return user

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")

        user = self.get_user(kwargs.get("uidb64"))

        if user is not None and default_token_generator.check_token(user, kwargs.get("token")):
            self.context["validlink"] = True
            self.context["title"] = "New Password"
            self.context["form"] = CustomUserSetPasswordForm(label_suffix="", user=user)
            return render(request=request, template_name="user/password-reset-confirm.html", context=self.context)
        else:
            messages.error(request=request, message="The password reset link is invalid or expired.")
            return redirect("password-reset")

    def post(self, request, *args, **kwargs):
        user = self.get_user(kwargs.get("uidb64"))

        if user is not None and default_token_generator.check_token(user, kwargs.get("token")):
            self.context["title"] = "New Password"
            self.context["form"] = CustomUserSetPasswordForm(label_suffix="", data=request.POST, user=user)

            if self.context["form"].is_valid():
                result = self.context["form"].save()

                if result:
                    custom_send_mail = CustomSendMail()
                    is_mail_send = custom_send_mail.send_mail(request=request,
                        subject         = "Your Password Has Been Changed",
                        template_name   = "user/password-change-email.html",
                        template_params = {"user":user, "title":"Your Password Changed"},
                        recipient_list  = [user.email],
                    )

                    if is_mail_send:
                        messages.success(request=request, message="The password has been reset successfully.")
                    else:
                        messages.error(request=request, message="The password has been reset but email not sent.")

                    return redirect("password-reset-complete")
                else:
                    messages.error(request=request, message="The password has not been reset. Try again.")

                return redirect("login")
        else:
            messages.error(request=request, message="The password reset link is invalid or expired.")
            return redirect("password-reset")

        return render(request=request, template_name="user/password-reset-confirm.html", context=self.context)

# User password reset complete view here.
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")

        self.context["title"] = "New Password"
        return render(request=request, template_name="user/password-reset-complete.html", context=self.context)

# Create Dashboard view here.
class UserDashboardView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        self.context["title"] = "Dashboard"

        self.context["active_admin_users"]   = User.objects.filter(is_superuser=True, is_staff=True, is_active=True).count()
        self.context["inactive_admin_users"] = User.objects.filter(is_superuser=True, is_staff=True, is_active=False).count()
        self.context["active_staff_users"]   = User.objects.filter(is_superuser=False, is_staff=True, is_active=True).count()
        self.context["inactive_staff_users"] = User.objects.filter(is_superuser=False, is_staff=True, is_active=False).count()
        self.context["active_students"]      = Student.objects.all().count()

        return render(request=request, template_name="user/dashboard.html", context=self.context)

# User create view here.
class UserCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm("auth.add_user"):
            messages.error(request=request, message="You do not have permission to access this page.")
            return redirect("dashboard")

        self.context["title"] = "Add User"
        self.context["form"] = CustomUserCreateForm(label_suffix="")
        return render(request=request, template_name="user/add-update-user.html", context=self.context)

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Add User"
        self.context["form"] = CustomUserCreateForm(request.POST, label_suffix="")

        if self.context["form"].is_valid():
            user = self.context["form"].save()

            if user:
                custom_send_mail = CustomSendMail()
                is_mail_send = custom_send_mail.send_mail(
                    request=request,
                    subject         = "Welcome to SMS",
                    recipient_list  = [user.email],
                    template_name   = "user/welcome-email.html",
                    template_params = {
                        "title":"Welcome to SMS",
                        "user":user,
                        "password":self.context["form"].cleaned_data.get("password1"),
                    }
                )

                if is_mail_send:
                    messages.success(request=request, message="The record has been saved successfully.")
                else:
                    messages.error(request=request, message="The record has been saved but email not sent.")

                return redirect("add-user")
            else:
                messages.error(request=request, message="The password has not been reset. Try again.")

        return render(request=request, template_name="user/add-update-user.html", context=self.context)

# User update view here.
class UserUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request, *args, **kwargs):
        try:
            if not request.user.has_perm("auth.change_user"):
                messages.error(request=request, message="You do not have permission to access this page.")
                return redirect("dashboard")

            user = User.objects.get(pk=kwargs.get("pk"))

            self.context["title"] = "Update User"
            self.context["form"] = CustomUserUpdateForm(instance=user, label_suffix="")

            return render(request=request, template_name="user/add-update-user.html", context=self.context)
        except User.DoesNotExist:
            messages.error(request=request, message="The record does not exist or has already been deleted.")
            return redirect("all-users")

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Update User"

        user = User.objects.get(pk=kwargs.get("pk"))
        self.context["form"] = CustomUserUpdateForm(request.POST, instance=user, label_suffix="")

        if self.context["form"].is_valid():
            user = self.context["form"].save()

            if user:
                messages.success(request=request, message="The record has been updated successfully.")
            else:
                messages.error(request=request, message="The record has not been updated. Try again.")
            return redirect("update-user", user.id)

        return render(request=request, template_name="user/add-update-user.html", context=self.context)

# User update profile view here.
class UserUpdateProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request, *args, **kwargs):
        try:
            if not request.user.has_perm("auth.change_user") and request.user.id != kwargs.get("pk"):
                messages.error(request=request, message="You do not have permission to access this page.")
                return redirect("dashboard")

            self.context["title"] = "Update Profile"
            user = User.objects.get(pk=kwargs.get("pk"))

            if request.user.is_superuser == True:
                self.context["form"] = CustomUpdateAdminProfileForm(instance=user, label_suffix="")
            else:
                self.context["form"] = CustomUpdateUserProfileForm(instance=user, label_suffix="")

            return render(request=request, template_name="user/update-profile.html", context=self.context)
        except User.DoesNotExist:
            messages.error(request=request, message="The record does not exist or has already been deleted.")
            return redirect("all-users")

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Update Profile"

        user = User.objects.get(pk=kwargs.get("pk"))

        if request.user.is_superuser == True:
            self.context["form"] = CustomUpdateAdminProfileForm(request.POST, instance=user, label_suffix="")
        else:
            self.context["form"] = CustomUpdateUserProfileForm(request.POST, instance=user, label_suffix="")

        if self.context["form"].is_valid():
            user = self.context["form"].save()

            if user:
                messages.success(request=request, message="Your profile has been updated successfully.")
            else:
                messages.error(request=request, message="Your profile has not been updated. Try again.")

            return redirect("update-profile", user.id)

        return render(request=request, template_name="user/update-profile.html", context=self.context)

# User list view here.
class UserListView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request):
        if not request.user.has_perm("auth.view_user") and not request.user.has_perm("auth.change_user") and not request.user.has_perm("auth.delete_user"):
            messages.error(request=request, message="You do not have permission to access this page.")
            return redirect("dashboard")

        per_page = request.GET.get("per-page", "10")

        if not per_page.isdigit() or int(per_page) <= 0:
            per_page = 10
        else:
            per_page = min(int(per_page), 100)

        user_lists = User.objects.all().order_by("id")
        paginator = Paginator(user_lists, per_page)
        current_page_number = request.GET.get("page")

        try:
            users = paginator.page(current_page_number)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        self.context["users"] = users
        self.context["per_page"] = per_page
        self.context["title"] = "All Users"

        return render(request, "user/all-users.html", self.context)

# User change password view here.
class UserChangePasswordView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request, *args, **kwargs):
        self.context["title"] = "Change Password"
        self.context["form"] = CustomUserChangePasswordForm(label_suffix="", user=request.user)
        return render(request=request, template_name="user/change-password.html", context=self.context)

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Change Password"
        self.context["form"] = CustomUserChangePasswordForm(label_suffix="", user=request.user, data=request.POST)

        if self.context["form"].is_valid():
            user = self.context["form"].save()

            if user:
                update_session_auth_hash(request, self.context["form"].user)
                messages.success(request=request, message="Your password has been changed successfully.")
            else:
                messages.error(request=request, message="Your password has not been changed. Try again.")

            return redirect("add-student")

        return render(request=request, template_name="user/change-password.html", context=self.context)

# User set password view here.
class UserSetPasswordView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request, *args, **kwargs):
        self.context["title"] = "Set Password"
        self.context["form"] = CustomUserSetPasswordForm(label_suffix="", user=request.user)
        return render(request=request, template_name="user/set-password.html", context=self.context)

    def post(self, request, *args, **kwargs):
        self.context["title"] = "Set Password"
        self.context["form"] = CustomUserSetPasswordForm(label_suffix="", user=request.user, data=request.POST)

        if self.context["form"].is_valid():
            user = self.context["form"].save()

            if user:
                update_session_auth_hash(request, self.context["form"].user)
                messages.success(request=request, message="Your password has been changed successfully.")
            else:
                messages.error(request=request, message="Your password has not been changed. Try again.")

            return redirect("add-student")

        return render(request=request, template_name="user/set-password.html", context=self.context)

# User logout view here.
class UserLogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        logout(request=request)

        if not request.user.is_authenticated:
            messages.success(request=request, message="You have successfully logged out.")
            return redirect("login")
        else:
            messages.error(request=request, message="You have not logged out. Try again.")
            return redirect("add-student")