# Import the base model class and field types from Django's ORM.
from django.db import models

# Import standard Python libraries for file handling and generating UUIDs.
import os, uuid

# Define a custom function to generate the file path for uploaded student images.
def student_image_upload_path(instance, filename):
    """
    Generate a unique file path for student images.

    Args:
        instance (Student): The instance of the Student model.
        filename (str): The original name of the uploaded file.

    Returns:
        str: A new file path to store the uploaded image.
    """

    # Extract the file extension from the original filename.
    ext = filename.split(".")[-1]

    # Generate a unique filename using UUID (e.g., student_abcd1234efgh5678.png).
    unique_filename = f"student_{uuid.uuid4().hex}.{ext}"

    # Return the complete relative path to save the image (MEDIA_ROOT/student/images/).
    return os.path.join("student/images/", unique_filename)

# Define the Student model representing a full student profile in the system.
class Student(models.Model):
    # ========== Student Personal Details ==========
    student_first_name = models.CharField(max_length=100, null=True)
    student_middle_name = models.CharField(max_length=100, null=True)
    student_last_name = models.CharField(max_length=100, null=True)

    # ========== Parent Information ==========
    student_father_first_name = models.CharField(max_length=100, null=True)
    student_father_middle_name = models.CharField(max_length=100, null=True)
    student_father_last_name = models.CharField(max_length=100, null=True)

    student_mother_first_name = models.CharField(max_length=100, null=True)
    student_mother_middle_name = models.CharField(max_length=100, null=True)
    student_mother_last_name = models.CharField(max_length=100, null=True)

    # ========== Contact Details ==========
    student_email = models.EmailField(max_length=100, null=True)
    student_phone_number = models.CharField(max_length=15, null=True)
    student_birth_date = models.DateField(null=True)
    student_gender = models.CharField(max_length=15, null=True)
    student_id = models.CharField(max_length=10, null=True)
    student_entry_year = models.CharField(max_length=100, null=True)
    student_semester = models.CharField(max_length=100, null=True)

    # ========== Address ==========
    student_address_line_1 = models.CharField(max_length=100, null=True)
    student_address_line_2 = models.CharField(max_length=100, null=True)
    student_city = models.CharField(max_length=100, null=True)
    student_state = models.CharField(max_length=100, null=True)
    student_country = models.CharField(max_length=100, null=True)
    student_zip = models.CharField(max_length=100, null=True)

    # ========== Image Upload ==========
    student_image = models.ImageField(upload_to=student_image_upload_path, null=True)
    # Uses custom path generation function defined above.

    # ========== Guardian Address ==========
    guardian_address_line_1 = models.CharField(max_length=100, null=True)
    guardian_address_line_2 = models.CharField(max_length=100, null=True)
    guardian_city = models.CharField(max_length=100, null=True)
    guardian_state = models.CharField(max_length=100, null=True)
    guardian_country = models.CharField(max_length=100, null=True)
    guardian_zip = models.CharField(max_length=100, null=True)

    # ========== First Emergency Contact ==========
    first_emergency_first_name = models.CharField(max_length=100, null=True)
    first_emergency_middle_name = models.CharField(max_length=100, null=True)
    first_emergency_last_name = models.CharField(max_length=100, null=True)
    first_emergency_phone_number = models.CharField(max_length=100, null=True)
    first_emergency_relationship = models.CharField(max_length=100, null=True)

    # ========== Second Emergency Contact ==========
    second_emergency_first_name = models.CharField(max_length=100, null=True)
    second_emergency_middle_name = models.CharField(max_length=100, null=True)
    second_emergency_last_name = models.CharField(max_length=100, null=True)
    second_emergency_phone_number = models.CharField(max_length=100, null=True)
    second_emergency_relationship = models.CharField(max_length=100, null=True)

    # ========== Physician Information ==========
    physician_first_name = models.CharField(max_length=100, null=True)
    physician_middle_name = models.CharField(max_length=100, null=True)
    physician_last_name = models.CharField(max_length=100, null=True)
    physician_primary_phone_number = models.CharField(max_length=100, null=True)
    physician_secondary_phone_number = models.CharField(max_length=100, null=True)
    preferred_hospital_name = models.CharField(max_length=100, null=True)
    physician_special_notes = models.TextField(null=True)

    # ========== Previous School Details ==========
    previous_school_name = models.CharField(max_length=100, null=True)
    previous_school_city = models.CharField(max_length=100, null=True)
    previous_school_state = models.CharField(max_length=100, null=True)
    previous_school_country = models.CharField(max_length=100, null=True)
    previous_school_date_started = models.DateField(null=True)
    previous_school_date_ended = models.DateField(null=True)
    previous_school_notes = models.TextField(null=True)