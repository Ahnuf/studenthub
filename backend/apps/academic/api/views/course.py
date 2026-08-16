from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from apps.academic.selectors.program_selector import ProgramSelector
from apps.academic.api.serializers.course import CourseReferenceSerializer
from apps.students.selectors.student_selector import StudentSelector


class CourseReferenceAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseReferenceSerializer

    def get_queryset(self):
        student = StudentSelector.get_profile(self.request.user)

        if student is None:
            raise NotFound("Student profile not found.")

        return ProgramSelector.list_program_courses(
            student.program,
        )