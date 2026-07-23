from django.urls import path

from apps.notes.views.note_view import (
    NoteListUploadAPIView,
    NoteDetailAPIView,
)

app_name = "notes"

urlpatterns = [
    path(
        "",
        NoteListUploadAPIView.as_view(),
        name="note-list-upload",
    ),
    path(
        "<int:note_id>/",
        NoteDetailAPIView.as_view(),
        name="note-detail",
    ),
]
