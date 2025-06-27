from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from .forms import StudentForm
from django.contrib import messages
from .models import Student
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin

file_storage = FileSystemStorage(location="/tmp/")

# Student create view here.
class StudentCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request):
        if not request.user.has_perm("student.add_student"):
            messages.error(request=request, message="You do not have permission to access this page.")
            return redirect("dashboard")

        self.context["title"] = "Add Student"
        self.context["form"] = StudentForm(label_suffix="")
        return render(request, "student/add-update-student.html", self.context)

    def post(self, request, *args, **kwargs):
        self.context["form"] = StudentForm(request.POST, request.FILES, label_suffix="")

        if self.context["form"].is_valid():
            student = self.context["form"].save()

            if student:
                messages.success(request=request, message="The record has been saved successfully.")
            else:
                messages.error(request=request, message="The record has not been saved. Try again.")

            return redirect("add-student")

        return render(request, "student/add-update-student.html", self.context)

# Student update view here.
class StudentUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request, *args, **kwargs):
        try:
            if not request.user.has_perm("student.change_student"):
                messages.error(request=request, message="You do not have permission to access this page.")
                return redirect("dashboard")

            student = Student.objects.get(pk=kwargs.get("pk"))
            self.context["title"] = "Update Student"
            self.context["student"] = student
            self.context["form"] = StudentForm(instance=student, label_suffix="")
            return render(request, "student/add-update-student.html", self.context)
        except Student.DoesNotExist:
            messages.error(request=request, message="The record does not exist or has already been deleted.")
            return redirect("all-students")

    def post(self, request, *args, **kwargs):
        student = Student.objects.get(pk=kwargs.get("pk"))
        self.context["form"] = StudentForm(request.POST, request.FILES, instance=student, label_suffix="")

        if self.context["form"].is_valid():
            student = self.context["form"].save()

            if student:
                messages.success(request=request, message="The record has been updated successfully.")
            else:
                messages.error(request=request, message="The record has not been updated. Try again.")

            return redirect("update-student", pk=kwargs.get("pk"))

        return render(request, "student/add-update-student.html", self.context)

# Student list view here.
class StudentListView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request):
        if not request.user.has_perm("student.view_student") and not request.user.has_perm("student.change_student") and not request.user.has_perm("student.delete_student"):
            messages.error(request=request, message="You do not have permission to access this page.")
            return redirect("dashboard")

        per_page = request.GET.get("per-page", "10")

        if not per_page.isdigit() or int(per_page) <= 0:
            per_page = 10
        else:
            per_page = min(int(per_page), 100)

        student_lists = Student.objects.all().order_by("id")
        paginator = Paginator(student_lists, per_page)
        current_page_number = request.GET.get("page")

        try:
            students = paginator.page(current_page_number)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        self.context["students"] = students
        self.context["per_page"] = per_page
        self.context["title"] = "All Students"

        return render(request, "student/all-students.html", self.context)

# Student detail view here.
class StudentDetailView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request, *args, **kwargs):
        try:
            if not request.user.has_perm("student.view_student"):
                messages.error(request=request, message="You do not have permission to access this page.")
                return redirect("dashboard")

            self.context["title"] = "Student Details"
            self.context["student"] = Student.objects.get(pk=kwargs.get("pk"))
            return render(request, "student/get-student.html", self.context)
        except Student.DoesNotExist:
            messages.error(request=request, message="The record does not exist or has already been deleted.")
            return redirect("all-students")

# Student delete view here.
class StudentDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    context = {}

    def get(self, request, *args, **kwargs):
        try:
            if not request.user.has_perm("student.delete_student"):
                messages.error(request=request, message="You do not have permission to access this page.")
                return redirect("dashboard")

            self.context["title"] = "Delete Student Confirmation"
            self.context["student"] = Student.objects.get(pk=kwargs.get("pk"))
            return render(request, "student/delete-student-confirmation.html", self.context)
        except Student.DoesNotExist:
            messages.error(request=request, message="The record does not exist or has already been deleted.")
            return redirect("all-students")

    def post(self, request, *args, **kwargs):
        try:
            self.context["student"] = Student.objects.get(pk=kwargs.get("pk"))
            deleted_count, deleted_object = self.context["student"].delete()

            if deleted_count > 0:
                messages.success(request=request, message="The record has been deleted successfully.")
            else:
                messages.error(request=request, message="The record has not been deleted. Try again.")
        except Student.DoesNotExist:
            messages.error(request=request, message="The record does not exist or has already been deleted.")

        return redirect("all-students")