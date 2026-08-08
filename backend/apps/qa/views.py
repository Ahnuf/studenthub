from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.throttling import ScopedRateThrottle
from apps.qa.selectors.QA_selector import QASelector
from apps.qa.services.QA_service import QAService
from apps.qa.serializers.QA_serializer import (
    QuestionCreateSerializer,
    QuestionListSerializer,
    QuestionDetailSerializer,
    AnswerCreateSerializer,
    AnswerDetailSerializer,
)
from core.api.responses import success_response


class QuestionListCreateAPIView(GenericAPIView):
    """
    List questions (optionally filtered by course_id), or post a
    new one.
    """

    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method == "POST":
            self.throttle_scope = "content_creation"
            return [ScopedRateThrottle()]

        return super().get_throttles()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return QuestionCreateSerializer

        return QuestionListSerializer

    def get(self, request, *args, **kwargs):
        course_id = request.query_params.get("course_id")

        questions = QASelector.list_questions(course_id=course_id)

        serializer = self.get_serializer(questions, many=True)

        return success_response(
            message="Questions fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        question = serializer.save()

        return success_response(
            message="Question posted successfully.",
            data=QuestionDetailSerializer(question).data,
            status_code=status.HTTP_201_CREATED,
        )


class QuestionDetailAPIView(GenericAPIView):
    """
    Retrieve a single question along with its answers.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = QuestionDetailSerializer

    def get(self, request, question_id, *args, **kwargs):
        question = QASelector.get_question(question_id)

        if question is None:
            raise NotFound("Question not found.")

        answers = QASelector.list_answers(question_id, user=request.user)

        return success_response(
            message="Question fetched successfully.",
            data={
                "question": self.get_serializer(question).data,
                "answers": AnswerDetailSerializer(answers, many=True).data,
            },
            status_code=status.HTTP_200_OK,
        )


class AnswerListCreateAPIView(GenericAPIView):
    """
    Post a new answer to a question. (Listing answers happens as
    part of QuestionDetailAPIView, since they're always viewed
    together with the question.)
    """

    permission_classes = [IsAuthenticated]
    serializer_class = AnswerCreateSerializer

    throttle_scope = "content_creation"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request, question_id, *args, **kwargs):
        question = QASelector.get_question(question_id)

        if question is None:
            raise NotFound("Question not found.")

        serializer = self.get_serializer(
            data=request.data,
            context={
                "request": request,
                "question": question,
            },
        )
        serializer.is_valid(raise_exception=True)

        answer = serializer.save()

        return success_response(
            message="Answer posted successfully.",
            data=AnswerDetailSerializer(answer).data,
            status_code=status.HTTP_201_CREATED,
        )


class AnswerAcceptAPIView(GenericAPIView):
    """
    Mark an answer as accepted. Only the question's asker may do
    this (enforced in QAService.accept_answer).
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, answer_id, *args, **kwargs):
        answer = QASelector.get_answer(answer_id)

        if answer is None:
            raise NotFound("Answer not found.")

        answer = QAService.accept_answer(answer, user=request.user)

        return success_response(
            message="Answer marked as accepted.",
            data=AnswerDetailSerializer(answer).data,
            status_code=status.HTTP_200_OK,
        )


class AnswerVoteAPIView(GenericAPIView):
    """
    Toggle the requesting user's upvote on an answer.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, answer_id, *args, **kwargs):
        answer = QASelector.get_answer(answer_id)

        if answer is None:
            raise NotFound("Answer not found.")

        result = QAService.toggle_upvote(answer, user=request.user)

        message = (
            "Upvote added." if result["has_voted"] else "Upvote removed."
        )

        return success_response(
            message=message,
            data=result,
            status_code=status.HTTP_200_OK,
        )