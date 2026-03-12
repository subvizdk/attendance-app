from django.db import models
from django.utils import timezone
from institutions.models import Batch
from students.models import Student

class AttendanceSession(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, related_name="attendance_sessions")
    date = models.DateField(default=timezone.localdate)
    label = models.CharField(max_length=50, default="Daily")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("batch", "date", "label")]
        ordering = ["-date", "label"]

    def __str__(self):
        return f"{self.batch} - {self.date} - {self.label}"

class AttendanceMark(models.Model):
    class Status(models.TextChoices):
        PRESENT = "P", "Present"
        ABSENT = "A", "Absent"
        LATE = "L", "Late"
        EXCUSED = "E", "Excused"

    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name="marks")
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="attendance_marks")
    status = models.CharField(max_length=1, choices=Status.choices)
    noted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("session", "student")]
        indexes = [models.Index(fields=["student", "session"])]
