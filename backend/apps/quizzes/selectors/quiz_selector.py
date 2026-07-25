from django.db.models import Count, Q

from apps.quizzes.models import (
    Quiz,
    QuizQuestion,
    QuizAttempt,
)

MAX_ATTEMPTS_PER_QUIZ = 5


class QuizSelector:
    """
    Read-only operations for quizzes, questions, and attempts.
    """

    # --- Quizzes ---

    @staticmethod
    def list_quizzes(course_id=None, query=None):
        queryset = (
            Quiz.objects
            .select_related("course", "creator")
            .filter(is_active=True)
            .annotate(question_count=Count("questions"))
        )

        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(course__title__icontains=query)
            )

        return queryset

    @staticmethod
    def get_quiz(quiz_id: int):
        return (
            Quiz.objects
            .select_related("course", "creator")
            .filter(id=quiz_id, is_active=True)
            .annotate(question_count=Count("questions"))
            .first()
        )

    # --- Questions ---

    @staticmethod
    def list_questions(quiz: Quiz):
        return (
            QuizQuestion.objects
            .filter(quiz=quiz)
            .prefetch_related("choices")
        )

    @staticmethod
    def get_question(quiz: Quiz, question_id: int):
        return (
            QuizQuestion.objects
            .filter(quiz=quiz, id=question_id)
            .prefetch_related("choices")
            .first()
        )

    @staticmethod
    def get_question_by_id(question_id: int):
        return (
            QuizQuestion.objects
            .select_related("quiz")
            .prefetch_related("choices")
            .filter(id=question_id)
            .first()
        )

    # --- Attempts ---

    @staticmethod
    def count_user_attempts(user, quiz: Quiz) -> int:
        return QuizAttempt.objects.filter(user=user, quiz=quiz).count()

    @staticmethod
    def get_attempt_status(user, quiz: Quiz) -> dict:
        attempts_used = QuizSelector.count_user_attempts(user, quiz)
        attempts_remaining = max(MAX_ATTEMPTS_PER_QUIZ - attempts_used, 0)

        return {
            "attempts_used": attempts_used,
            "attempts_remaining": attempts_remaining,
            "can_attempt": attempts_remaining > 0,
        }

    @staticmethod
    def list_attempts(user, quiz: Quiz):
        return (
            QuizAttempt.objects
            .filter(user=user, quiz=quiz)
        )

    @staticmethod
    def get_attempt(user, attempt_id: int):
        """
        An attempt is personal, not shared -- scoped strictly to
        the user who took it. None (-> 404) if missing or belongs
        to someone else.
        """

        return (
            QuizAttempt.objects
            .select_related("quiz")
            .prefetch_related("answers__question", "answers__selected_choice")
            .filter(user=user, id=attempt_id)
            .first()
        )