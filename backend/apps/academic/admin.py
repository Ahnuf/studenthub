from django.contrib import admin
from .models import University, Program, Course
from .models import Course, Program, ProgramCourse, University, AcademicSession



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


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "short_title",
        "is_active",
    )

    search_fields = (
        "title",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    ordering = (
        "title",
    )


@admin.register(ProgramCourse)
class ProgramCourseAdmin(admin.ModelAdmin):
    list_display = (
        "course_code",
        "course",
        "program",
        "recommended_semester",
        "theory_credit_hours",
        "lab_credit_hours",
        "total_credit_hours",
        "category",
        "is_active",
    )

    search_fields = (
        "course_code",
        "course__title",
        "program__program_name",
        "program__university__short_name",
    )

    list_filter = (
        "program__university",
        "category",
        "recommended_semester",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    ordering = (
        "program",
        "recommended_semester",
        "course_code",
    )


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = (
        "term",
        "year",
        "university",
        "start_date",
        "end_date",
        "is_current",
        "is_active",
    )

    search_fields = (
        "university__name",
        "university__short_name",
        "year",
    )

    list_filter = (
        "term",
        "year",
        "university",
        "is_current",
        "is_active",
    )

    list_editable = (
        "is_current",
        "is_active",
    )

    ordering = (
        "-year",
        "term",
    )