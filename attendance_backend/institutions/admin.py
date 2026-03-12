from django.contrib import admin
from .models import Branch, Level, Batch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)
    ordering = ("order", "name")

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("name", "branch", "level", "year", "is_active")
    list_filter = ("branch", "level", "year", "is_active")
    search_fields = ("name",)
