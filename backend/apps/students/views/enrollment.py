from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.students.models import StudentProfile
from apps.students.serializers.enrollment import (
    EnrollmentCreateSerializer,
    EnrollmentResponseSerializer,
)


class EnrollmentCreateAPIView(GenericAPIView):
    """
    API for creating a student enrollment.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentCreateSerializer

    def post(self, request, *args, **kwargs):
        student_profile = StudentProfile.objects.select_related(
            "program",
            "university",
        ).get(user=request.user)

        serializer = self.get_serializer(
            data=request.data,
            context={
                "student_profile": student_profile,
            },
        )

        serializer.is_valid(raise_exception=True)

        enrollment = serializer.save()

        response_serializer = EnrollmentResponseSerializer(enrollment)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )