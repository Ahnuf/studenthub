from django.contrib import admin

from apps.notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course",
        "main_heading",
        "uploader",
        "is_active",
        "created_at",
    )
    list_filter = (
        "is_active",
        "course",
    )
    search_fields = (
        "main_heading",
        "sub_heading",
        "course__title",
        "uploader__email",
    )
    ordering = ("-created_at",)
