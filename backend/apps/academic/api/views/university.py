from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.academic.api.serializers.university import UniversityReferenceSerializer
from apps.academic.selectors.academic_selector import AcademicSelector


class UniversityReferenceAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UniversityReferenceSerializer

    def get_queryset(self):
        return AcademicSelector.list_universities()