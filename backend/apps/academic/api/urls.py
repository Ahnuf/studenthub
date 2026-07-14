from django.urls import path

from apps.academic.api.views import (
    AcademicSessionReferenceAPIView,
    ProgramReferenceAPIView,
    UniversityReferenceAPIView,
)

app_name = "academic"

urlpatterns = [
    path(
        "universities/",
        UniversityReferenceAPIView.as_view(),
        name="universities",
    ),
    path(
        "programs/",
        ProgramReferenceAPIView.as_view(),
        name="programs",
    ),
    path(
        "sessions/",
        AcademicSessionReferenceAPIView.as_view(),
        name="sessions",
    ),
]