from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Branch(models.Model):
    name = models.CharField(max_length=120, unique=True)
    city = models.CharField(max_length=120)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name} ({self.city})'


class Level(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='levels')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('branch', 'name')
        ordering = ['branch__name', 'name']

    def __str__(self) -> str:
        return f'{self.branch.name} - {self.name}'


class Batch(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='batches')
    name = models.CharField(max_length=120)
    academic_year = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('level', 'name', 'academic_year')
        ordering = ['-academic_year', 'level__name', 'name']

    def clean(self) -> None:
        if self.start_date >= self.end_date:
            raise ValidationError('Batch end date must be later than start date.')

    def __str__(self) -> str:
        return f'{self.name} ({self.academic_year})'


class Student(models.Model):
    admission_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    date_of_birth = models.DateField(null=True, blank=True)
    current_batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        related_name='students',
        help_text='A student can be assigned to only one active batch at a time.',
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['admission_number']

    def __str__(self) -> str:
        return f'{self.admission_number} - {self.first_name} {self.last_name}'


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LATE = 'late', 'Late'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.localdate)
    status = models.CharField(max_length=10, choices=Status.choices)
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date', 'student__admission_number']

    def __str__(self) -> str:
        return f'{self.student.admission_number} {self.date} - {self.status}'
