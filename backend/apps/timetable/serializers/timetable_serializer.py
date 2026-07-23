from rest_framework import serializers

from apps.timetable.models import TimetableEntry
from apps.timetable.services.timetable_service import TimetableService


class TimetableEntryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimetableEntry
        exclude = (
            "user",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        user = self.context["request"].user

        return TimetableService.create_entry(
            user=user,
            **validated_data,
        )


class TimetableEntryDetailSerializer(serializers.ModelSerializer):

    day_of_week_display = serializers.CharField(
        source="get_day_of_week_display",
        read_only=True,
    )

    class Meta:
        model = TimetableEntry
        fields = (
            "id",
            "course_name",
            "day_of_week",
            "day_of_week_display",
            "start_time",
            "end_time",
            "location",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class TimetableEntryUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimetableEntry
        exclude = (
            "user",
            "created_at",
            "updated_at",
        )

    def update(self, instance, validated_data):
        return TimetableService.update_entry(
            instance,
            **validated_data,
        )