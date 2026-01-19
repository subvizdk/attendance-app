from django.db import models
from core.models import Branch
from academics.models import Batch, Student

class Exam(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="exams")
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="exams")
    title = models.CharField(max_length=200)
    date = models.DateField()
    max_marks = models.IntegerField(default=100)

    STATUS_CHOICES = (
        ("DRAFT", "DRAFT"),
        ("PUBLISHED", "PUBLISHED"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")

    def __str__(self):
        return self.title

class Mark(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="marks")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="marks")
    marks_obtained = models.FloatField(default=0)
    note = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        unique_together = ("exam", "student")