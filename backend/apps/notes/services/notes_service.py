from django.contrib.postgres.search import SearchVector
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.notes.models import Note
from apps.notes.text_extraction import extract_text


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

        note.extracted_text = extract_text(note.file)
        note.save()

        NoteService._refresh_search_vector(note)

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

        file_changed = (
            "file" in validated_data
            and validated_data["file"] != note.file
        )

        for field, value in validated_data.items():
            setattr(note, field, value)

        try:
            note.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        if file_changed:
            note.extracted_text = extract_text(note.file)

        note.save()

        NoteService._refresh_search_vector(note)

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

    @staticmethod
    def _refresh_search_vector(note: Note) -> None:
        """
        Recompute the note's Postgres search_vector from its
        content fields, weighted so a heading match ranks above a
        match buried in extracted file text.

        Done as a separate .update() (not part of note.save()) so
        Postgres builds the tsvector server-side in one query,
        rather than round-tripping the (potentially large)
        extracted_text through Python.
        """

        vector = (
            SearchVector("main_heading", weight="A")
            + SearchVector("sub_heading", weight="B")
            + SearchVector("description", weight="C")
            + SearchVector("extracted_text", weight="D")
        )

        Note.objects.filter(pk=note.pk).update(search_vector=vector)