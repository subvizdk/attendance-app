from django.contrib import admin
from .models import Student, StudentBatchAssignment

class StudentBatchAssignmentInline(admin.TabularInline):
    model = StudentBatchAssignment
    extra = 0
    autocomplete_fields = ["batch"]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "first_name", "last_name", "is_active")
    search_fields = ("student_id", "first_name", "last_name")
    list_filter = ("is_active",)
    inlines = [StudentBatchAssignmentInline]

@admin.register(StudentBatchAssignment)
class StudentBatchAssignmentAdmin(admin.ModelAdmin):
    list_display = ("student", "batch", "started_at", "ended_at")
    list_filter = ("batch__branch", "batch__year", "ended_at", "batch__level")
    search_fields = ("student__student_id", "student__first_name", "student__last_name", "batch__name")
