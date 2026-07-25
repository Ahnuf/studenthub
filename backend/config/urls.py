from django.contrib import admin
from django.urls import path, include
from config.api import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{API_PREFIX}/auth/", include("apps.accounts.api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(f"{API_PREFIX}/students/", include("apps.students.urls")),
    path(f"{API_PREFIX}/academic/",include("apps.academic.api.urls")),
    path(f"{API_PREFIX}/assignments/",include("apps.assignments.urls")),
    path(f"{API_PREFIX}/timetable/",include("apps.timetable.urls")),
    path("api/v1/qa/", include("apps.QA.urls")),
    path("api/v1/quiz/", include("apps.quizzes.urls")),
    path("api/v1/notes/", include("apps.notes.urls")),
    path("api/v1/flashcards/", include("apps.flashcards.urls")),
]