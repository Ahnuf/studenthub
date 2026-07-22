from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import IsTeacherOrAdmin
from apps.students.serializers.result_serializer import (
    PublishResultSerializer,
)
from apps.students.services.result_service import (
    StudentResultService,
)
from core.api.responses import success_response


class PublishResultView(GenericAPIView):
    """
    Publish a student's course result.
    """

    permission_classes = [
        IsAuthenticated,
        IsTeacherOrAdmin,
    ]
    serializer_class = PublishResultSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        student_course = (
            StudentResultService.publish_result(
                student_course_id=serializer.validated_data[
                    "student_course_id"
                ],
                marks=serializer.validated_data[
                    "marks"
                ],
            )
        )

        return success_response(
            message="Result published successfully.",
            data={
                "student_course_id": student_course.id,
                "grade": student_course.grade,
                "marks": student_course.marks,
                "status": student_course.status,
            },
            status_code=status.HTTP_200_OK,
        )