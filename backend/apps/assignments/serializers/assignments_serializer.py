from rest_framework import serializers

from apps.assignments.models import Assignment
from apps.assignments.services.assignment_service import AssignmentService


class AssignmentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        exclude = (
            "user",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        user = self.context["request"].user

        return AssignmentService.create_assignment(
            user=user,
            **validated_data,
        )


class AssignmentDetailSerializer(serializers.ModelSerializer):

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Assignment
        fields = (
            "id",
            "course_name",
            "title",
            "description",
            "due_date",
            "status",
            "status_display",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class AssignmentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        exclude = (
            "user",
            "created_at",
            "updated_at",
        )

    def update(self, instance, validated_data):
        return AssignmentService.update_assignment(
            instance,
            **validated_data,
        )
