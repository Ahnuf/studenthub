from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from apps.timetable.selectors.timetable_selector import TimetableSelector
from apps.timetable.services.timetable_service import TimetableService
from apps.timetable.serializers.timetable_serializer import (
    TimetableEntryCreateSerializer,
    TimetableEntryDetailSerializer,
    TimetableEntryUpdateSerializer,
)
from core.api.responses import success_response


def _build_conflict_warnings(entry) -> list[str]:
    """
    Turn any overlapping entries into human-readable warning
    strings. Empty list means no conflicts -- never blocks a save.
    """

    conflicts = TimetableService.get_conflicts(entry)

    return [
        (
            f"This overlaps with '{conflict.course_name}' "
            f"({conflict.start_time.strftime('%H:%M')}-"
            f"{conflict.end_time.strftime('%H:%M')}) "
            f"on {conflict.get_day_of_week_display()}."
        )
        for conflict in conflicts
    ]


class TimetableListCreateAPIView(GenericAPIView):
    """
    List the authenticated user's timetable entries, or create a
    new one.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TimetableEntryCreateSerializer

        return TimetableEntryDetailSerializer

    def get(self, request, *args, **kwargs):
        entries = TimetableSelector.list_entries(request.user)

        serializer = self.get_serializer(entries, many=True)

        return success_response(
            message="Timetable fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        entry = serializer.save()

        warnings = _build_conflict_warnings(entry)

        message = "Timetable entry created successfully."

        if warnings:
            message = (
                "Timetable entry created successfully, "
                "but it conflicts with your existing schedule."
            )

        return success_response(
            message=message,
            data={
                **TimetableEntryDetailSerializer(entry).data,
                "warnings": warnings,
            },
            status_code=status.HTTP_201_CREATED,
        )


class TimetableDetailAPIView(GenericAPIView):
    """
    Retrieve, update, or delete a single timetable entry.

    Always scoped to the requesting user -- an entry belonging to
    another user returns 404, never 403.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return TimetableEntryUpdateSerializer

        return TimetableEntryDetailSerializer

    def get_entry(self, request, entry_id):
        entry = TimetableSelector.get_entry(
            user=request.user,
            entry_id=entry_id,
        )

        if entry is None:
            raise NotFound("Timetable entry not found.")

        return entry

    def get(self, request, entry_id, *args, **kwargs):
        entry = self.get_entry(request, entry_id)

        serializer = self.get_serializer(entry)

        return success_response(
            message="Timetable entry fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def patch(self, request, entry_id, *args, **kwargs):
        entry = self.get_entry(request, entry_id)

        serializer = self.get_serializer(
            entry,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()

        warnings = _build_conflict_warnings(entry)

        message = "Timetable entry updated successfully."

        if warnings:
            message = (
                "Timetable entry updated successfully, "
                "but it conflicts with your existing schedule."
            )

        return success_response(
            message=message,
            data={
                **TimetableEntryDetailSerializer(entry).data,
                "warnings": warnings,
            },
            status_code=status.HTTP_200_OK,
        )

    def delete(self, request, entry_id, *args, **kwargs):
        entry = self.get_entry(request, entry_id)

        TimetableService.delete_entry(entry)

        return success_response(
            message="Timetable entry deleted successfully.",
            status_code=status.HTTP_200_OK,
        )