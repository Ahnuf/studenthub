from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.models import TimeStampedModel
from apps.academic.models import Course


class Question(TimeStampedModel):
    """
    A student's question about a Course, open to any authenticated
    user to answer -- the free, human-powered alternative to the
    (budget-blocked) AI Tutor. Visibility mirrors Notes: shared
    across universities/programs for the same underlying Course.
    """

    asker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="questions",
    )

    title = models.CharField(
        max_length=200,
    )

    body = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    @property
    def is_resolved(self) -> bool:
        return self.answers.filter(is_accepted=True).exists()

    def __str__(self):
        return f"{self.course} - {self.title}"


class Answer(TimeStampedModel):
    """
    An answer to a Question. Exactly one answer per question may be
    marked accepted -- enforced both by the service layer (only the
    asker may accept) and by the DB constraint below, so it can
    never end up in an inconsistent state even from a bug elsewhere.
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    body = models.TextField()

    is_accepted = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-is_accepted", "-created_at"]
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        constraints = [
            models.UniqueConstraint(
                fields=["question"],
                condition=models.Q(is_accepted=True),
                name="unique_accepted_answer_per_question",
            )
        ]

    def clean(self):
        if self.user_id == self.question.asker_id:
            raise ValidationError(
                {
                    "user": (
                        "You cannot answer your own question."
                    )
                }
            )

    def __str__(self):
        marker = " (accepted)" if self.is_accepted else ""
        return f"{self.question.title} - answer by {self.user}{marker}"


class AnswerVote(TimeStampedModel):
    """
    A single user's upvote on an Answer. Existence of the row IS
    the vote -- there's no direction/value, just present or absent.
    The unique constraint is what actually prevents double-voting;
    a bare counter on Answer couldn't do that on its own.
    """

    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="votes",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answer_votes",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["answer", "user"],
                name="unique_vote_per_user_per_answer",
            )
        ]
        verbose_name = "Answer Vote"
        verbose_name_plural = "Answer Votes"

    def __str__(self):
        return f"{self.user} upvoted answer #{self.answer_id}"