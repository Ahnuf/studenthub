from rest_framework import serializers


class PublishResultSerializer(serializers.Serializer):
    student_course_id = serializers.IntegerField(
        min_value=1,
    )

    marks = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )