from django.db import models
from django.db.models import Q
from institutions.models import Batch

class Student(models.Model):
    student_id = models.CharField(max_length=40, unique=True)  # roll no / id
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}".strip()

class StudentBatchAssignment(models.Model):
    # Keeps history, enforces: only 1 active assignment per student
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="batch_assignments")
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, related_name="student_assignments")
    started_at = models.DateField()
    ended_at = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student"],
                condition=Q(ended_at__isnull=True),
                name="unique_active_batch_per_student",
            )
        ]
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.student} -> {self.batch}"
