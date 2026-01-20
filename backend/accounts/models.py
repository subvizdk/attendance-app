from django.db import models
from django.contrib.auth.models import User
from core.models import Branch


class Profile(models.Model):
    ROLE_SUPER_ADMIN = "SUPER_ADMIN"
    ROLE_BRANCH_ADMIN = "BRANCH_ADMIN"
    ROLE_TEACHER = "TEACHER"
    ROLE_STUDENT = "STUDENT"  # later

    ROLE_CHOICES = [
        (ROLE_SUPER_ADMIN, "Super Admin"),
        (ROLE_BRANCH_ADMIN, "Branch Admin"),
        (ROLE_TEACHER, "Teacher/Staff"),
        (ROLE_STUDENT, "Student"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_TEACHER)

    # default branch (auto branch)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"