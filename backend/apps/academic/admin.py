from django.contrib import admin

from .models import University


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