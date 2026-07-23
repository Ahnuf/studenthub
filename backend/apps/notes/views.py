from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from apps.notes.selectors.notes_selector import NoteSelector
from apps.notes.services.notes_service import NoteService
from apps.notes.serializers.notes_serializer import (
    NoteUploadSerializer,
    NoteDetailSerializer,
    NoteUpdateSerializer,
)
from core.api.responses import success_response


class NoteListUploadAPIView(GenericAPIView):
    """
    List/search notes (shared, any authenticated user), or upload
    a new one.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NoteUploadSerializer

        return NoteDetailSerializer

    def get(self, request, *args, **kwargs):
        course_id = request.query_params.get("course_id")
        query = request.query_params.get("q")

        notes = NoteSelector.list_notes(
            course_id=course_id,
            query=query,
        )

        serializer = self.get_serializer(notes, many=True)

        return success_response(
            message="Notes fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        note = serializer.save()

        return success_response(
            message="Note uploaded successfully.",
            data=NoteDetailSerializer(note).data,
            status_code=status.HTTP_201_CREATED,
        )


class NoteDetailAPIView(GenericAPIView):
    """
    Retrieve any active note (shared/public to authenticated
    users). Update/delete are restricted to the uploader -- a
    mismatch raises 403 (existence is already public via search).
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return NoteUpdateSerializer

        return NoteDetailSerializer

    def get_note(self, note_id):
        note = NoteSelector.get_note(note_id)

        if note is None:
            raise NotFound("Note not found.")

        return note

    def get(self, request, note_id, *args, **kwargs):
        note = self.get_note(note_id)

        serializer = self.get_serializer(note)

        return success_response(
            message="Note fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def patch(self, request, note_id, *args, **kwargs):
        note = self.get_note(note_id)

        serializer = self.get_serializer(
            note,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        note = serializer.save()

        return success_response(
            message="Note updated successfully.",
            data=NoteDetailSerializer(note).data,
            status_code=status.HTTP_200_OK,
        )

    def delete(self, request, note_id, *args, **kwargs):
        note = self.get_note(note_id)

        NoteService.delete_note(note, user=request.user)

        return success_response(
            message="Note deleted successfully.",
            status_code=status.HTTP_200_OK,
        )
