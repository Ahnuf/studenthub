from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from apps.common.permissions import IsStudent
from apps.students.selectors.student_selector import StudentSelector
from apps.students.services.academic_progress_service import AcademicProgressService
from apps.students.serializers.academic_progress_serializer import (
    AcademicProgressDashboardSerializer,
)
from core.api.responses import success_response


class AcademicProgressDashboardView(GenericAPIView):
    """
    Returns the authenticated student's academic progress dashboard.
    """

    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]
    serializer_class = AcademicProgressDashboardSerializer

    def get(self, request, *args, **kwargs):
        student = StudentSelector.get_profile(request.user)

        if student is None:
            raise NotFound("Student profile not found.")

        dashboard = AcademicProgressService.build_dashboard(student)

        serializer = self.get_serializer(dashboard)

        return success_response(
            message="Academic progress fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )