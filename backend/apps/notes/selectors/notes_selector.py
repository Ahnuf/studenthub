from django.contrib.postgres.search import SearchQuery, SearchRank

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
        queryset = (
            Note.objects
            .select_related("course", "uploader")
            .filter(is_active=True)
        )

        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)

        if query:
            search_query = SearchQuery(query, search_type="websearch")
            queryset = (
                queryset
                .filter(search_vector=search_query)
                .annotate(rank=SearchRank("search_vector", search_query))
                .order_by("-rank", "-created_at")
            )

        return queryset

    @staticmethod
    def get_note(note_id: int):
        return (
            Note.objects
            .select_related("course", "uploader")
            .filter(id=note_id, is_active=True)
            .first()
        )

    @staticmethod
    def list_my_notes(user):
        return (
            Note.objects
            .select_related("course")
            .filter(uploader=user)
        )

    @staticmethod
    def list_recent_for_courses(course_ids: list[int], limit: int = 5):
        """
        Return the most recent active notes for a set of courses --
        used by the Academic Progress Dashboard to show "recent
        notes for your current courses". Empty course_ids returns
        nothing rather than every note on the platform.
        """

        if not course_ids:
            return Note.objects.none()

        return (
            Note.objects
            .select_related("course", "uploader")
            .filter(is_active=True, course_id__in=course_ids)
            .order_by("-created_at")[:limit]
        )