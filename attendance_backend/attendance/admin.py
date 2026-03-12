from django.contrib import admin
from .models import AttendanceSession, AttendanceMark

class AttendanceMarkInline(admin.TabularInline):
    model = AttendanceMark
    extra = 0
    autocomplete_fields = ["student"]

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ("batch", "date", "label", "created_at")
    list_filter = ("date", "label", "batch__branch", "batch__year", "batch__level")
    search_fields = ("batch__name",)
    inlines = [AttendanceMarkInline]

@admin.register(AttendanceMark)
class AttendanceMarkAdmin(admin.ModelAdmin):
    list_display = ("session", "student", "status", "noted_at")
    list_filter = ("status", "session__date", "session__batch__branch", "session__batch__level")
    search_fields = ("student__student_id", "student__first_name", "student__last_name")
