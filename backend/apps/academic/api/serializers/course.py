from rest_framework import serializers

from apps.academic.models import ProgramCourse


class CourseReferenceSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = ProgramCourse
        fields = (
            "id",
            "course",
            "title",
            "course_code",
            "recommended_semester",
            "category",
        )