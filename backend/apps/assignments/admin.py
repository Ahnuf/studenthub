from django.contrib import admin

from apps.assignments.models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course_name",
        "title",
        "due_date",
        "status",
    )
    list_filter = (
        "status",
    )
    search_fields = (
        "course_name",
        "title",
        "user__email",
    )
    ordering = ("due_date",)