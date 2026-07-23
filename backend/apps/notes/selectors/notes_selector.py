from django.db.models import Q

from apps.notes.models import Note


class NoteSelector:
    """
    Read-only operations for notes.

    Unlike Assignments/Timetable, these are NOT scoped to a single
    user for reads -- notes are shared. Only get_note() restricts
    to is_active=True (soft-deleted/hidden notes are invisible to
    everyone, including the uploader, via this method).
    """

    @staticmethod
    def list_notes(course_id=None, query=None):
        """
        Return active notes, optionally filtered by course and/or
        a free-text search against heading/sub-heading/course
        title.
        """

        queryset = (
            Note.objects
            .select_related(
                "course",
                "uploader",
            )
            .filter(
                is_active=True,
            )
        )

        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)

        if query:
            queryset = queryset.filter(
                Q(main_heading__icontains=query)
                | Q(sub_heading__icontains=query)
                | Q(course__title__icontains=query)
            )

        return queryset

    @staticmethod
    def get_note(note_id: int):
        """
        Return a single active note by ID, visible to any
        authenticated user. None (-> 404) if missing or inactive.
        """

        return (
            Note.objects
            .select_related(
                "course",
                "uploader",
            )
            .filter(
                id=note_id,
                is_active=True,
            )
            .first()
        )

    @staticmethod
    def list_my_notes(user):
        """
        Return all notes uploaded by the given user, including
        inactive ones -- this is the uploader's own management
        view, not the public search.
        """

        return (
            Note.objects
            .select_related(
                "course",
            )
            .filter(
                uploader=user,
            )
        )
