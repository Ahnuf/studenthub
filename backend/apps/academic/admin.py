from django.contrib import admin

from .models import University, Program


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = (
        "short_name",
        "name",
        "city",
        "country",
        "is_active",
    )

    search_fields = (
        "name",
        "short_name",
    )

    list_filter = (
        "country",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    ordering = ("name",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "program_name",
        "degree_type",
        "university",
        "duration_years",
        "study_system",
        "is_active",
    )

    search_fields = (
        "program_name",
        "university__name",
        "university__short_name",
    )

    list_filter = (
        "degree_type",
        "study_system",
        "university",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    ordering = (
        "university",
        "degree_type",
        "program_name",
    )