from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.qa.models import Answer, AnswerVote, Question
from apps.qa.selectors.QA_selector import QASelector


class QAService:
    """
    Business logic for Course Q&A.
    """

    @staticmethod
    @transaction.atomic
    def create_question(user, **validated_data) -> Question:
        question = Question(
            asker=user,
            **validated_data,
        )

        try:
            question.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        question.save()

        return question

    @staticmethod
    @transaction.atomic
    def create_answer(question: Question, user, **validated_data) -> Answer:
        answer = Answer(
            question=question,
            user=user,
            **validated_data,
        )

        try:
            answer.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        answer.save()

        return answer

    @staticmethod
    @transaction.atomic
    def accept_answer(answer: Answer, user) -> Answer:
        """
        Mark an answer as the accepted one for its question.

        Only the original asker may do this. If a different answer
        was previously accepted, it's un-accepted first -- the DB
        constraint would reject two accepted rows at once anyway,
        but doing it explicitly here keeps the intent clear and
        avoids relying on the constraint to catch a logic error.
        """

        if answer.question.asker_id != user.id:
            raise PermissionDenied(
                "Only the person who asked the question can "
                "mark an answer as accepted."
            )

        Answer.objects.filter(
            question=answer.question,
            is_accepted=True,
        ).exclude(pk=answer.pk).update(is_accepted=False)

        answer.is_accepted = True
        answer.save(update_fields=["is_accepted", "updated_at"])

        return answer

    @staticmethod
    @transaction.atomic
    def toggle_upvote(answer: Answer, user) -> dict:
        """
        Toggle the requesting user's upvote on an answer.

        Returns {"has_voted": bool, "vote_count": int} so the view
        can respond without a second query round-trip for the count.
        """

        if answer.user_id == user.id:
            raise PermissionDenied(
                "You cannot upvote your own answer."
            )

        existing_vote = AnswerVote.objects.filter(
            answer=answer,
            user=user,
        ).first()

        if existing_vote is not None:
            existing_vote.delete()
            has_voted = False
        else:
            AnswerVote.objects.create(answer=answer, user=user)
            has_voted = True

        vote_count = AnswerVote.objects.filter(answer=answer).count()

        return {
            "has_voted": has_voted,
            "vote_count": vote_count,
        }