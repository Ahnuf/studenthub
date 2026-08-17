from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.throttling import ScopedRateThrottle
from apps.quizzes.selectors.quiz_selector import QuizSelector
from apps.quizzes.services.quiz_service import QuizService
from apps.quizzes.serializers.quiz_serializer import (
    QuizCreateSerializer,
    QuizListSerializer,
    QuizDetailSerializer,
    QuizUpdateSerializer,
    QuizQuestionPublicSerializer,
    QuizQuestionCreateSerializer,
    QuizQuestionUpdateSerializer,
    SubmitAttemptSerializer,
    QuizAttemptSerializer,
)
from core.api.responses import success_response


class QuizListCreateAPIView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method == "POST":
            self.throttle_scope = "content_creation"
            return [ScopedRateThrottle()]

        return super().get_throttles()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return QuizCreateSerializer
        return QuizListSerializer

    def get(self, request, *args, **kwargs):
        course_id = request.query_params.get("course_id")
        query = request.query_params.get("q")

        quizzes = QuizSelector.list_quizzes(
            course_id=course_id,
            query=query,
        )

        serializer = self.get_serializer(
            quizzes,
            many=True,
            context={"request": request},
        )

        return success_response(
            message="Quizzes fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        quiz = serializer.save()

        return success_response(
            message="Quiz created successfully.",
            data=QuizDetailSerializer(
                QuizSelector.get_quiz(quiz.id), context={"request": request}
            ).data,
            status_code=status.HTTP_201_CREATED,
        )


class QuizQuestionDetailAPIView(GenericAPIView):
    """
    GET/PATCH/DELETE a single question.
    GET is creator-only because it exposes the answer key.
    PATCH/DELETE are also creator-only through the service layer.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = QuizQuestionUpdateSerializer

    def get_question(self, question_id):
        question = QuizSelector.get_question_by_id(question_id)

        if question is None:
            raise NotFound("Question not found.")

        return question

    def get(self, request, question_id, *args, **kwargs):
        question = self.get_question(question_id)

        if question.quiz.creator_id != request.user.id:
            raise NotFound("Question not found.")

        return success_response(
            message="Question fetched successfully.",
            data=QuizQuestionCreatorSerializer(
                question,
            ).data,
            status_code=status.HTTP_200_OK,
        )

    def patch(self, request, question_id, *args, **kwargs):
        question = self.get_question(question_id)

        serializer = self.get_serializer(
            question,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        question = serializer.save()

        return success_response(
            message="Question updated successfully.",
            data=QuizQuestionPublicSerializer(
                question,
            ).data,
            status_code=status.HTTP_200_OK,
        )

    def delete(self, request, question_id, *args, **kwargs):
        question = self.get_question(question_id)

        QuizService.delete_question(
            question,
            user=request.user,
        )

        return success_response(
            message="Question deleted successfully.",
            status_code=status.HTTP_200_OK,
        )


class QuizQuestionListCreateAPIView(GenericAPIView):
    """
    List questions for taking the quiz (no answer key), or add a
    new question with its choices (creator only).
    """

    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method == "POST":
            self.throttle_scope = "content_creation"
            return [ScopedRateThrottle()]

        return super().get_throttles()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return QuizQuestionCreateSerializer
        return QuizQuestionPublicSerializer

    def get_quiz(self, quiz_id):
        quiz = QuizSelector.get_quiz(quiz_id)
        if quiz is None:
            raise NotFound("Quiz not found.")
        return quiz

    def get(self, request, quiz_id, *args, **kwargs):
        quiz = self.get_quiz(quiz_id)

        questions = QuizSelector.list_questions(quiz)

        serializer = QuizQuestionPublicSerializer(questions, many=True)

        return success_response(
            message="Questions fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request, quiz_id, *args, **kwargs):
        quiz = self.get_quiz(quiz_id)

        serializer = self.get_serializer(
            data=request.data,
            context={"request": request, "quiz": quiz},
        )
        serializer.is_valid(raise_exception=True)

        question = serializer.save()

        return success_response(
            message="Question added successfully.",
            data=QuizQuestionPublicSerializer(question).data,
            status_code=status.HTTP_201_CREATED,
        )


class QuizQuestionDetailAPIView(GenericAPIView):
    """
    Update/delete a single question. Creator only.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = QuizQuestionUpdateSerializer

    def get_question(self, question_id):
        question = QuizSelector.get_question_by_id(question_id)
        if question is None:
            raise NotFound("Question not found.")
        return question

    def patch(self, request, question_id, *args, **kwargs):
        question = self.get_question(question_id)

        serializer = self.get_serializer(
            question, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        question = serializer.save()

        return success_response(
            message="Question updated successfully.",
            data=QuizQuestionPublicSerializer(question).data,
            status_code=status.HTTP_200_OK,
        )

    def delete(self, request, question_id, *args, **kwargs):
        question = self.get_question(question_id)

        QuizService.delete_question(question, user=request.user)

        return success_response(
            message="Question deleted successfully.",
            status_code=status.HTTP_200_OK,
        )


class QuizAttemptListSubmitAPIView(GenericAPIView):
    """
    Submit a full attempt (answers to every question at once), or
    list the requesting user's own past attempts for this quiz.
    """

    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method == "POST":
            self.throttle_scope = "quiz_attempt"
            return [ScopedRateThrottle()]

        return super().get_throttles()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubmitAttemptSerializer
        return QuizAttemptSerializer

    def get_quiz(self, quiz_id):
        quiz = QuizSelector.get_quiz(quiz_id)
        if quiz is None:
            raise NotFound("Quiz not found.")
        return quiz

    def get(self, request, quiz_id, *args, **kwargs):
        quiz = self.get_quiz(quiz_id)

        attempts = QuizSelector.list_attempts(request.user, quiz)

        serializer = QuizAttemptSerializer(attempts, many=True)

        return success_response(
            message="Attempts fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request, quiz_id, *args, **kwargs):
        quiz = self.get_quiz(quiz_id)

        serializer = self.get_serializer(
            data=request.data,
            context={"request": request, "quiz": quiz},
        )
        serializer.is_valid(raise_exception=True)

        attempt = serializer.save()

        return success_response(
            message="Quiz submitted successfully.",
            data=QuizAttemptSerializer(attempt).data,
            status_code=status.HTTP_201_CREATED,
        )


class QuizAttemptDetailAPIView(GenericAPIView):
    """
    Review a single past attempt in detail. Personal, not shared --
    404 (not 403) if it belongs to someone else, since unlike
    Notes/QA content, attempt history was never publicly visible
    to begin with.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = QuizAttemptSerializer

    def get(self, request, attempt_id, *args, **kwargs):
        attempt = QuizSelector.get_attempt(request.user, attempt_id)

        if attempt is None:
            raise NotFound("Attempt not found.")

        serializer = self.get_serializer(attempt)

        return success_response(
            message="Attempt fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )