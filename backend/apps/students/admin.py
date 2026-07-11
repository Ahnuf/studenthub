from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "university",
        "program",
        "current_semester",
        "academic_status",
    )

    search_fields = (
        "user__username",
        "user__email",
        "registration_number",
        "roll_number",
    )

    list_filter = (
        "university",
        "program",
        "academic_status",
        "current_semester",
    )

    autocomplete_fields = (
        "user",
        "university",
        "program",
        "joined_session",
    )

    ordering = (
        "university",
        "program",
    )