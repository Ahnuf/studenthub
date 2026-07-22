from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.academic.models import AcademicSession, ProgramCourse
from apps.students.models import (
    AcademicStatus,
    Enrollment,
    StudentCourse,
    StudentProfile,
    EnrollmentStatus,
    CourseStatus
)
from apps.students.selectors.enrollment_selector import EnrollmentSelector


class EnrollmentService:
    """
    Handles the complete student course enrollment workflow.
    """

    @staticmethod
    @transaction.atomic
    def create_enrollment(
        student: StudentProfile,
        academic_session: AcademicSession,
        program_course_ids: list[int],
    ) -> Enrollment:
        """
        Create a new enrollment for a student.
        """

        program_courses = list(
        EnrollmentSelector.get_program_courses(
            program_course_ids
            )
        )

        EnrollmentService._validate_student_eligibility(
        student=student,
        academic_session=academic_session,
        )

        EnrollmentService._validate_duplicate_courses(
            program_course_ids
        )

        EnrollmentService._validate_course_selection(
            student=student,
            program_courses=program_courses,
            program_course_ids=program_course_ids,
        )

        total_credit_hours = (
            EnrollmentService._calculate_credit_hours(
                program_courses
            )
        )

        enrollment = EnrollmentService._create_enrollment(
            student=student,
            academic_session=academic_session,
            total_credit_hours=total_credit_hours,
        )

        EnrollmentService._create_student_courses(
            enrollment=enrollment,
            program_courses=program_courses,
        )

        return enrollment

    @staticmethod
    def _create_student_courses(
        enrollment: Enrollment,
        program_courses: list[ProgramCourse],
        ):
            """
            Create StudentCourse records for the enrollment.
            """

            for program_course in program_courses:
                student_course = StudentCourse(
                    enrollment=enrollment,
                    program_course=program_course,
                    semester_taken=enrollment.semester,
                    attempt_number=1,
                    status=CourseStatus.ENROLLED,
                    )

                student_course.full_clean()
                student_course.save()

    @staticmethod
    def _calculate_credit_hours(
    program_courses: list[ProgramCourse],
    ) -> int:
        """
        Calculate the total credit hours for the selected courses.
        """

        return sum(
            course.total_credit_hours
            for course in program_courses
        )

    @staticmethod
    def _create_enrollment(
        student: StudentProfile,
        academic_session: AcademicSession,
        total_credit_hours: int,
    ) -> Enrollment:
        """
        Create and persist an Enrollment record.
        """

        enrollment = Enrollment(
            student=student,
            academic_session=academic_session,
            semester=student.current_semester,
            total_credit_hours=total_credit_hours,
            status=EnrollmentStatus.SUBMITTED,
        )

        enrollment.full_clean()
        enrollment.save()

        return enrollment


    @staticmethod
    def _validate_duplicate_courses(
        program_course_ids: list[int],
    ):
        """
        Ensure the same course is not selected multiple times.
        """

        if len(program_course_ids) != len(set(program_course_ids)):
            raise ValidationError(
                {
                    "program_course_ids": (
                        "Duplicate courses are not allowed."
                    )
                }
            )

    @staticmethod
    def _validate_student_eligibility(
        student: StudentProfile,
        academic_session: AcademicSession,
    ):
        """
        Validate whether the student is eligible to enroll.
        """

        if student.academic_status != AcademicStatus.ACTIVE:
            raise ValidationError(
                {
                    "student": (
                        "Only active students can enroll."
                    )
                }
            )

        enrollment = EnrollmentSelector.get_enrollment(
            student=student,
            academic_session=academic_session,
        )

        if enrollment is not None:
            raise ValidationError(
                {
                    "enrollment": (
                        "The student already has an enrollment "
                        "for this academic session."
                    )
                }
            )


    @staticmethod
    def _validate_course_selection(
    student: StudentProfile,
    program_courses: list[ProgramCourse],
    program_course_ids: list[int],
    ):
        """
        Validate the selected courses.
        """

        if len(program_courses) != len(program_course_ids):
            raise ValidationError(
                {
                    "program_course_ids": (
                        "One or more selected courses do not exist."
                    )
                }
            )

        for program_course in program_courses:

            if program_course.program != student.program:
                raise ValidationError(
                    {
                        "program_course_ids": (
                            f"{program_course.course_code} "
                            "does not belong to the student's program."
                        )
                    }
                )

        completed_courses = (
            EnrollmentSelector.list_completed_courses(student)
        )

        completed_ids = {
            course.program_course_id
            for course in completed_courses
        }

        for program_course in program_courses:

            if program_course.id in completed_ids:
                raise ValidationError(
                    {
                        "program_course_ids": (
                            f"{program_course.course_code} "
                            "has already been passed."
                        )
                    }
                )