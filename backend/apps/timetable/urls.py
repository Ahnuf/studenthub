from django.urls import path

from apps.timetable.views import (
    TimetableListCreateAPIView,
    TimetableDetailAPIView,
)

app_name = "timetable"

urlpatterns = [
    path(
        "",
        TimetableListCreateAPIView.as_view(),
        name="timetable-list-create",
    ),
    path(
        "<int:entry_id>/",
        TimetableDetailAPIView.as_view(),
        name="timetable-detail",
    ),
]