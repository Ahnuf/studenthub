from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from core.models import TimeStampedModel
from apps.academic.models import Course

ALLOWED_NOTE_EXTENSIONS = [
    "pdf", "doc", "docx", "ppt", "pptx", "jpg", "jpeg", "png",
]

# Only these types actually have extractable text. Images are
# allowed as uploads (e.g. a photographed whiteboard) but contribute
# nothing to extracted_text -- OCR is a separate, later feature.
EXTRACTABLE_EXTENSIONS = ["pdf", "doc", "docx", "ppt", "pptx"]

MAX_NOTE_FILE_SIZE_MB = 20


class Note(TimeStampedModel):
    """
    A student-uploaded note attached to a Course.

    Upload is personal (tracked via `uploader`), but visibility is
    shared -- any authenticated student can view/search any active
    note, regardless of university or program, as long as it's the
    same underlying Course. See docs/11-notes.md for the reasoning.
    """

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="notes",
    )

    main_heading = models.CharField(
        max_length=200,
    )

    sub_heading = models.CharField(
        max_length=200,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    file = models.FileField(
        upload_to="notes/%Y/%m/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=ALLOWED_NOTE_EXTENSIONS,
            )
        ],
    )

    is_active = models.BooleanField(
        default=True,
    )

    # --- Search-related fields (never serialized/exposed to users) ---

    extracted_text = models.TextField(
        blank=True,
        editable=False,
        help_text=(
            "Text pulled from the uploaded file at save time. "
            "Used only for search; never returned by the API."
        ),
    )

    search_vector = SearchVectorField(
        null=True,
        editable=False,
        help_text="Postgres full-text search index, kept in sync via NoteService.",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        indexes = [
            GinIndex(fields=["search_vector"], name="note_search_vector_idx"),
        ]

    def clean(self):
        self._validate_file_size()

    def _validate_file_size(self):
        if not self.file:
            return

        max_bytes = MAX_NOTE_FILE_SIZE_MB * 1024 * 1024

        if self.file.size > max_bytes:
            raise ValidationError(
                {
                    "file": (
                        f"File size must not exceed "
                        f"{MAX_NOTE_FILE_SIZE_MB}MB."
                    )
                }
            )

    def __str__(self):
        return f"{self.course} - {self.main_heading}"