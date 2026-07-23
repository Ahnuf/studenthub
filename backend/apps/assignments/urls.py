from django.urls import path

from apps.assignments.views.assignments_view import (
    AssignmentListCreateAPIView,
    AssignmentDetailAPIView,
)

app_name = "assignments"

urlpatterns = [
    path(
        "",
        AssignmentListCreateAPIView.as_view(),
        name="assignment-list-create",
    ),
    path(
        "<int:assignment_id>/",
        AssignmentDetailAPIView.as_view(),
        name="assignment-detail",
    ),
]