from rest_framework import serializers

from apps.notes.models import Note
from apps.notes.services.notes_service import NoteService


class NoteUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = (
            "course",
            "main_heading",
            "sub_heading",
            "description",
            "file",
        )

    def create(self, validated_data):
        user = self.context["request"].user

        return NoteService.create_note(
            user=user,
            **validated_data,
        )


class NoteDetailSerializer(serializers.ModelSerializer):

    course_title = serializers.CharField(
        source="course.title",
        read_only=True,
    )

    uploaded_by = serializers.CharField(
        source="uploader.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Note
        fields = (
            "id",
            "course",
            "course_title",
            "main_heading",
            "sub_heading",
            "description",
            "file",
            "uploaded_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class NoteUpdateSerializer(serializers.ModelSerializer):
    """
    Course is intentionally excluded -- a note stays attached to
    the course it was uploaded under. Only content fields and the
    file itself can be changed.
    """

    class Meta:
        model = Note
        fields = (
            "main_heading",
            "sub_heading",
            "description",
            "file",
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user

        return NoteService.update_note(
            instance,
            user=user,
            **validated_data,
        )
