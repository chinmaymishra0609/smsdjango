from django import forms
from django.core.exceptions import ValidationError
from .models import Student

# Create Student form here.
class StudentForm(forms.ModelForm):
    GENDER   = [("", "---------"), ("male","Male"), ("female","Female"), ("other","Other")]    
    SEMESTER = [("", "---------"), ("first","First"), ("second","Second"), ("third","Third"), ("fourth","Fourth")]

    student_first_name               = forms.CharField(label="First Name", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_middle_name              = forms.CharField(label="Middle Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_last_name                = forms.CharField(label="Last Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_father_first_name        = forms.CharField(label="Father First Name", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_father_middle_name       = forms.CharField(label="Father Middle Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_father_last_name         = forms.CharField(label="Father Last Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_mother_first_name        = forms.CharField(label="Mother First Name", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_mother_middle_name       = forms.CharField(label="Mother Middle Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_mother_last_name         = forms.CharField(label="Mother Last Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_email                    = forms.CharField(label="Email", required=True, widget=forms.EmailInput(attrs={"class":"form-control"}))
    student_phone_number             = forms.CharField(label="Phone Number", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_birth_date               = forms.CharField(label="Birth Date", required=True, widget=forms.DateInput(attrs={"class":"form-control", "type": "date"}))
    student_gender                   = forms.ChoiceField(label="Gender", required=True, choices=GENDER, widget=forms.Select(attrs={"class":"form-select"}))
    student_id                       = forms.CharField(label="Student ID", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_entry_year               = forms.CharField(label="Entry Year", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_semester                 = forms.ChoiceField(label="Semester", required=True, choices=SEMESTER, widget=forms.Select(attrs={"class":"form-select"}))
    student_address_line_1           = forms.CharField(label="Address Line 1", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_address_line_2           = forms.CharField(label="Address Line 2", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_city                     = forms.CharField(label="City", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_state                    = forms.CharField(label="State", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_country                  = forms.CharField(label="Country", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_zip                      = forms.CharField(label="ZIP", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    student_image                    = forms.ImageField(label="Image", required=True, widget=forms.ClearableFileInput(attrs={"class":"form-control"}))

    guardian_address_line_1          = forms.CharField(label="Address Line 1", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_address_line_2          = forms.CharField(label="Address Line 2", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_city                    = forms.CharField(label="City", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_state                   = forms.CharField(label="State", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_country                 = forms.CharField(label="Country", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    guardian_zip                     = forms.CharField(label="ZIP Code", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))

    first_emergency_first_name       = forms.CharField(label="First Name", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_emergency_middle_name      = forms.CharField(label="Middle Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_emergency_last_name        = forms.CharField(label="Last Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_emergency_phone_number     = forms.CharField(label="Phone Number", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_emergency_relationship     = forms.CharField(label="Relationship", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))

    second_emergency_first_name      = forms.CharField(label="First Name", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    second_emergency_middle_name     = forms.CharField(label="Middle Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    second_emergency_last_name       = forms.CharField(label="Last Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    second_emergency_phone_number    = forms.CharField(label="Phone Number", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    second_emergency_relationship    = forms.CharField(label="Relationship", required=True, widget=forms.TextInput(attrs={"class":"form-control"}))

    physician_first_name             = forms.CharField(label="First Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    physician_middle_name            = forms.CharField(label="Middle Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    physician_last_name              = forms.CharField(label="Last Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    physician_primary_phone_number   = forms.CharField(label="Primary Phone", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    physician_secondary_phone_number = forms.CharField(label="Secondary Phone", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    preferred_hospital_name          = forms.CharField(label="Preferred Hospital", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    physician_special_notes          = forms.CharField(label="Special Notes", required=False, widget=forms.Textarea(attrs={"class":"form-control", "rows":3}))

    previous_school_name             = forms.CharField(label="Name", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    previous_school_city             = forms.CharField(label="City", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    previous_school_state            = forms.CharField(label="State", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    previous_school_country          = forms.CharField(label="Country", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    previous_school_date_started     = forms.CharField(label="Start Date", required=False, widget=forms.DateInput(attrs={"class":"form-control", "type": "date"}))
    previous_school_date_ended       = forms.CharField(label="End Date", required=False, widget=forms.DateInput(attrs={"class":"form-control", "type": "date"}))
    previous_school_notes            = forms.CharField(label="Special Notes", required=False, widget=forms.Textarea(attrs={"class":"form-control", "rows":3}))

    class Meta:
        model = Student
        fields = "__all__"

    def clean_student_gender(self):
        value = self.cleaned_data.get("student_gender")

        if value is not None:
            if value not in ["male", "female", "other"]:
                raise ValidationError("Invalid gender selected.")
        return value

    def clean_student_semester(self):
        value = self.cleaned_data.get("student_semester")

        if value is not None:
            if value not in ["first", "second", "third", "fourth"]:
                raise ValidationError("Invalid semester selected.")
        return value