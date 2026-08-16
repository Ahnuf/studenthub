from django.urls import path

from apps.academic.api.views import (
    AcademicSessionReferenceAPIView,
    CourseReferenceAPIView,
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
    path(
        "courses/",
        CourseReferenceAPIView.as_view(),
        name="courses",
    ),
]