from django.contrib import admin

from .models import Enrollment, StudentCourse, StudentProfile




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


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "academic_session",
        "semester",
        "status",
        "total_credit_hours",
    )

    list_filter = (
        "status",
        "academic_session",
        "semester",
    )

    search_fields = (
        "student__user__username",
        "student__user__email",
        "student__registration_number",
        "student__roll_number",
    )

    autocomplete_fields = (
        "student",
        "academic_session",
    )

    ordering = (
        "-academic_session__start_date",
    )


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):

    list_display = (
        "enrollment",
        "program_course",
        "semester_taken",
        "attempt_number",
        "status",
        "grade",
    )

    list_filter = (
        "status",
        "semester_taken",
        "enrollment__academic_session",
    )

    search_fields = (
        "enrollment__student__user__username",
        "enrollment__student__user__email",
        "program_course__course__title",
        "program_course__course__course_code",
    )

    autocomplete_fields = (
        "enrollment",
        "program_course",
    )

    ordering = (
        "-created_at",
    )