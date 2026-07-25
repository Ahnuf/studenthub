from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.models import TimeStampedModel
from apps.academic.models import Course


class Quiz(TimeStampedModel):
    """
    A student-authored quiz for a Course. Shared platform-wide,
    same visibility model as Notes/QA/Flashcards.
    """

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quizzes",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="quizzes",
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"{self.course} - {self.title}"


class QuizQuestion(TimeStampedModel):
    """
    A single MCQ prompt belonging to a Quiz.
    """

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    text = models.TextField()

    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Quiz Question"
        verbose_name_plural = "Quiz Questions"

    def __str__(self):
        return f"{self.quiz} - Q{self.order}"


class QuizChoice(TimeStampedModel):
    """
    One answer option for a QuizQuestion. Exactly one choice per
    question may be marked correct -- enforced at the DB level
    (same pattern as Answer.is_accepted in the QA app), so it can
    never end up inconsistent even from a bug elsewhere.
    """

    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name="choices",
    )

    text = models.CharField(max_length=255)

    is_correct = models.BooleanField(default=False)

    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Quiz Choice"
        verbose_name_plural = "Quiz Choices"
        constraints = [
            models.UniqueConstraint(
                fields=["question"],
                condition=models.Q(is_correct=True),
                name="unique_correct_choice_per_question",
            )
        ]

    def __str__(self):
        marker = " (correct)" if self.is_correct else ""
        return f"{self.text}{marker}"


class QuizAttempt(TimeStampedModel):
    """
    A single completed attempt at a quiz. Deliberately stores raw
    counts, not just a percentage -- this is a historical record
    of what happened at submission time, not something that should
    silently change if the quiz's questions are edited afterward.
    """

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
    )

    total_questions = models.PositiveSmallIntegerField()

    correct_answers = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"

    @property
    def score_percentage(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return round((self.correct_answers / self.total_questions) * 100, 2)

    def __str__(self):
        return (
            f"{self.user} - {self.quiz} - "
            f"{self.correct_answers}/{self.total_questions}"
        )


class QuizAttemptAnswer(TimeStampedModel):
    """
    One question's answer within a completed attempt. `is_correct`
    is a snapshot taken at submission time -- like QuizAttempt
    itself, this must never be recalculated later from the live
    QuizChoice data, since the quiz's content could change after
    the fact.

    question/selected_choice use PROTECT: once a question has been
    attempted by anyone, its content becomes historical record and
    shouldn't be silently deletable out from under that history.
    """

    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.PROTECT,
        related_name="attempt_answers",
    )

    selected_choice = models.ForeignKey(
        QuizChoice,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
    )

    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["question__order"]
        verbose_name = "Quiz Attempt Answer"
        verbose_name_plural = "Quiz Attempt Answers"
        constraints = [
            models.UniqueConstraint(
                fields=["attempt", "question"],
                name="unique_answer_per_question_per_attempt",
            )
        ]

    def clean(self):
        if (
            self.selected_choice_id
            and self.selected_choice.question_id != self.question_id
        ):
            raise ValidationError(
                {
                    "selected_choice": (
                        "Selected choice does not belong to this question."
                    )
                }
            )

    def __str__(self):
        return f"Attempt #{self.attempt_id} - Q{self.question.order}"