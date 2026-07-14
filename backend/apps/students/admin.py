from django.contrib import admin
from .models import StudentProfile, StudentCourse


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


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = (
        "student_profile",
        "program_course",
        "academic_session",
        "semester_taken",
        "attempt_number",
        "status",
        "grade",
    )

    list_filter = (
        "status",
        "academic_session",
        "semester_taken",
    )

    search_fields = (
        "student_profile__user__username",
        "student_profile__user__email",
        "program_course__course__title",
        "program_course__course_code",
    )

    autocomplete_fields = (
        "student_profile",
        "program_course",
        "academic_session",
    )

    ordering = (
        "-academic_session",
        "student_profile",
    )