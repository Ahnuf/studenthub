from django.urls import path    
from apps.students.views.student_profile import StudentProfileAPIView


app_name = "students"

urlpatterns = [
    path(
        "profile/",
        StudentProfileAPIView.as_view(),
        name="student-profile",
    ),
]