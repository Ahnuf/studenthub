from django.db.models import Count, Exists, OuterRef

from apps.QA.models import Answer, AnswerVote, Question


class QASelector:
    """
    Read-only operations for Course Q&A.
    """

    @staticmethod
    def list_questions(course_id=None):
        """
        Return questions, optionally filtered by course, annotated
        with answer_count so list views don't need N+1 queries.
        """

        queryset = (
            Question.objects
            .select_related("course", "asker")
            .annotate(answer_count=Count("answers"))
        )

        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)

        return queryset

    @staticmethod
    def get_question(question_id: int):
        return (
            Question.objects
            .select_related("course", "asker")
            .filter(id=question_id)
            .first()
        )

    @staticmethod
    def list_answers(question_id: int, user=None):
        """
        Return answers for a question, annotated with vote_count
        and (if a user is given) whether that user has voted --
        ordering already puts accepted first, then by vote_count.
        """

        queryset = (
            Answer.objects
            .select_related("user")
            .filter(question_id=question_id)
            .annotate(vote_count=Count("votes"))
        )

        if user is not None and user.is_authenticated:
            queryset = queryset.annotate(
                has_voted=Exists(
                    AnswerVote.objects.filter(
                        answer=OuterRef("pk"),
                        user=user,
                    )
                )
            )

        return queryset.order_by("-is_accepted", "-vote_count", "created_at")

    @staticmethod
    def get_answer(answer_id: int):
        return (
            Answer.objects
            .select_related("question", "user")
            .filter(id=answer_id)
            .first()
        )