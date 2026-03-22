from django.contrib import admin

from .models import AttendanceRecord, Batch, Branch, Level, Student


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'description')
    list_filter = ('branch',)
    search_fields = ('name', 'branch__name')


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'level', 'is_active', 'start_date', 'end_date')
    list_filter = ('academic_year', 'is_active', 'level__branch')
    search_fields = ('name', 'level__name', 'level__branch__name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'first_name', 'last_name', 'current_batch', 'is_active')
    list_filter = ('is_active', 'current_batch__academic_year', 'current_batch__level__branch')
    search_fields = ('admission_number', 'first_name', 'last_name')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'remarks')
    list_filter = ('date', 'status', 'student__current_batch__level__branch')
    search_fields = ('student__admission_number', 'student__first_name', 'student__last_name')
