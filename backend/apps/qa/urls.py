from django.urls import path

from apps.qa.views import (
    QuestionListCreateAPIView,
    QuestionDetailAPIView,
    AnswerListCreateAPIView,
    AnswerAcceptAPIView,
    AnswerVoteAPIView,
)

app_name = "qa"

urlpatterns = [
    path(
        "questions/",
        QuestionListCreateAPIView.as_view(),
        name="question-list-create",
    ),
    path(
        "questions/<int:question_id>/",
        QuestionDetailAPIView.as_view(),
        name="question-detail",
    ),
    path(
        "questions/<int:question_id>/answers/",
        AnswerListCreateAPIView.as_view(),
        name="answer-create",
    ),
    path(
        "answers/<int:answer_id>/accept/",
        AnswerAcceptAPIView.as_view(),
        name="answer-accept",
    ),
    path(
        "answers/<int:answer_id>/vote/",
        AnswerVoteAPIView.as_view(),
        name="answer-vote",
    ),
]