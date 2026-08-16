from django.urls import path

from apps.qa.views import (
    QuestionListCreateAPIView,
    QuestionDetailAPIView,
    AnswerListCreateAPIView,
    AnswerAcceptAPIView,
    AnswerVoteAPIView,
    QuestionModerationAPIView,
    AnswerModerationAPIView,
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
    path(
    "questions/<int:question_id>/moderate/",
    QuestionModerationAPIView.as_view(),
    name="question-moderate",
    ),

    path(
        "answers/<int:answer_id>/moderate/",
        AnswerModerationAPIView.as_view(),
        name="answer-moderate",
    ),
]