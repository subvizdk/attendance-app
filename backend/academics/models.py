from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

from core.models import Institution, Branch


class Course(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=200)
    grade_level = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return self.name


class Batch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="batches")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="batches")
    year = models.IntegerField()
    label = models.CharField(max_length=120)  # e.g. "Morning A"

    def __str__(self):
        return f"{self.course.name} - {self.label} ({self.year})"


class Student(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="students")

    admission_no = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)

    father_full_name = models.CharField(max_length=200, blank=True, default="")
    mother_full_name = models.CharField(max_length=200, blank=True, default="")

    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")

    class Meta:
        unique_together = ("branch", "admission_no")

    def __str__(self):
        return f"{self.full_name} ({self.admission_no})"


class StudentEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="enrollments", null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # null means active

    class Meta:
        constraints = [
            # Only one ACTIVE enrollment per student (end_date is NULL)
            models.UniqueConstraint(
                fields=["student"],
                condition=Q(end_date__isnull=True),
                name="uniq_active_enrollment_per_student",
            )
        ]

    def __str__(self):
        return f"{self.student.full_name} -> {self.batch}"


class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments")
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="teacher_assignments")
    can_take_attendance = models.BooleanField(default=True)
    can_enter_marks = models.BooleanField(default=True)

    class Meta:
        unique_together = ("teacher", "batch")