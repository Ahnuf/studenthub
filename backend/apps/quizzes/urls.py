from django.urls import path

from apps.quizzes.views import (
    QuizListCreateAPIView,
    QuizDetailAPIView,
    QuizQuestionListCreateAPIView,
    QuizQuestionDetailAPIView,
    QuizAttemptListSubmitAPIView,
    QuizAttemptDetailAPIView,
)

app_name = "quizzes"

urlpatterns = [
    path("", QuizListCreateAPIView.as_view(), name="quiz-list-create"),
    path("<int:quiz_id>/", QuizDetailAPIView.as_view(), name="quiz-detail"),
    path(
        "<int:quiz_id>/questions/",
        QuizQuestionListCreateAPIView.as_view(),
        name="question-list-create",
    ),
    path(
        "questions/<int:question_id>/",
        QuizQuestionDetailAPIView.as_view(),
        name="question-detail",
    ),
    path(
        "<int:quiz_id>/attempts/",
        QuizAttemptListSubmitAPIView.as_view(),
        name="attempt-list-submit",
    ),
    path(
        "attempts/<int:attempt_id>/",
        QuizAttemptDetailAPIView.as_view(),
        name="attempt-detail",
    ),
]