from django.urls import path    
from apps.students.views.student_profile import StudentProfileAPIView
from apps.students.views.enrollment import EnrollmentCreateAPIView


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
]