from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.academic.api.serializers.program import ProgramReferenceSerializer
from apps.academic.selectors.academic_selector import AcademicSelector


class ProgramReferenceAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramReferenceSerializer

    def get_queryset(self):
        university_id = self.request.query_params.get("university")

        if not university_id:
            raise ValidationError(
                {
                    "university": [
                        "This query parameter is required."
                    ]
                }
            )

        return AcademicSelector.list_programs(
            university_id=university_id
        )