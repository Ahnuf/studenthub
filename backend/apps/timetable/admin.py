from django.contrib import admin

from apps.timetable.models import TimetableEntry


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course_name",
        "day_of_week",
        "start_time",
        "end_time",
        "location",
    )
    list_filter = (
        "day_of_week",
    )
    search_fields = (
        "course_name",
        "user__email",
    )
    ordering = ("day_of_week", "start_time")