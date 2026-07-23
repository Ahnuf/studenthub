from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.notes.models import Note


class NoteService:
    """
    Business logic for note operations.
    """

    @staticmethod
    @transaction.atomic
    def create_note(user, **validated_data) -> Note:
        """
        Create a new note uploaded by the given user.
        """

        note = Note(
            uploader=user,
            **validated_data,
        )

        try:
            note.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        note.save()

        return note

    @staticmethod
    @transaction.atomic
    def update_note(note: Note, user, **validated_data) -> Note:
        """
        Update an existing note. Only the uploader may update it --
        a mismatch raises 403, since the note's existence is
        already publicly known (unlike Assignments/Timetable).
        """

        NoteService._check_ownership(note, user)

        validated_data.pop("uploader", None)

        for field, value in validated_data.items():
            setattr(note, field, value)

        try:
            note.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        note.save()

        return note

    @staticmethod
    @transaction.atomic
    def delete_note(note: Note, user) -> None:
        """
        Delete a note. Only the uploader may delete it.
        """

        NoteService._check_ownership(note, user)

        note.delete()

    @staticmethod
    def _check_ownership(note: Note, user):
        if note.uploader_id != user.id:
            raise PermissionDenied(
                "You can only modify your own notes."
            )
