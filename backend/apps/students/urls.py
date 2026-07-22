from django.urls import path    
from apps.students.views.student_profile import StudentProfileAPIView
from apps.students.views.enrollment import EnrollmentCreateAPIView
from .views.transcript_view import TranscriptView
from apps.students.views.result_view import PublishResultView
from apps.students.views.academic_progress_view import AcademicProgressDashboardView


app_name = "students"

urlpatterns = [
    path(
        "profile/",
        StudentProfileAPIView.as_view(),
        name="student-profile",
    ),
    path(
        "enrollments/",
        EnrollmentCreateAPIView.as_view(),
        name="student-enrollment"
    ),
    path(
        "me/transcript/",
        TranscriptView.as_view(),
        name="student-transcript",
    ),
    path(
        "results/publish/",
        PublishResultView.as_view(),
        name="publish-result",
    ),
    path("academic-progress/", AcademicProgressDashboardView.as_view())
]