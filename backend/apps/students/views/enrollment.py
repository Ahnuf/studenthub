from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from apps.common.permissions import IsStudent
from apps.students.selectors.student_selector import StudentSelector
from apps.students.serializers.enrollment import (
    EnrollmentCreateSerializer,
    EnrollmentResponseSerializer,
)
from core.api.responses import success_response


class EnrollmentCreateAPIView(GenericAPIView):
    """
    API for creating a student enrollment.
    """

    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]
    serializer_class = EnrollmentCreateSerializer

    def post(self, request, *args, **kwargs):
        student_profile = StudentSelector.get_profile(request.user)

        if student_profile is None:
            raise NotFound("Student profile not found.")

        serializer = self.get_serializer(
            data=request.data,
            context={
                "student_profile": student_profile,
            },
        )

        serializer.is_valid(raise_exception=True)

        enrollment = serializer.save()

        response_serializer = EnrollmentResponseSerializer(enrollment)

        return success_response(
            message="Enrollment created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )