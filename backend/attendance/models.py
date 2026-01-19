from django.db import models
from django.contrib.auth.models import User
from core.models import Branch
from academics.models import Batch, Student

class AttendanceSession(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="attendance_sessions")
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="attendance_sessions")
    date = models.DateField()
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    STATUS_CHOICES = (
        ("DRAFT", "DRAFT"),
        ("SUBMITTED", "SUBMITTED"),
        ("LOCKED", "LOCKED"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")

    class Meta:
        unique_together = ("batch", "date")

class AttendanceRecord(models.Model):
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name="records")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")

    STATUS_CHOICES = (
        ("PRESENT", "PRESENT"),
        ("ABSENT", "ABSENT"),
        ("LATE", "LATE"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PRESENT")
    note = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        unique_together = ("session", "student")
