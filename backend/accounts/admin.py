from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "branch")
    list_filter = ("role", "branch")
    search_fields = ("user__username",)
