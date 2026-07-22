from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from apps.common.permissions import IsStudent
from apps.students.selectors.student_selector import StudentSelector
from apps.students.serializers.transcript_serializer import (
    TranscriptSerializer,
)
from apps.students.services.transcript_service import (
    TranscriptService,
)


class TranscriptView(GenericAPIView):
    """
    Retrieve the authenticated student's transcript.
    """

    permission_classes = [
        IsAuthenticated,
        IsStudent,
    ]
    serializer_class = TranscriptSerializer

    def get(self, request, *args, **kwargs):
        student = StudentSelector.get_profile(request.user)

        if student is None:
            raise NotFound("Student profile not found.")

        transcript = TranscriptService.get_transcript(
            student=student,
        )

        serializer = self.get_serializer(transcript)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )