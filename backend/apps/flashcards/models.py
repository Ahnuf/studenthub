from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from apps.academic.models import Course


class ProgressStatus(models.TextChoices):
    STILL_LEARNING = "STILL_LEARNING", "Still Learning"
    KNOWN = "KNOWN", "Known"


class FlashcardDeck(TimeStampedModel):
    """
    A named collection of flashcards for a course. Shared
    platform-wide, same visibility model as Notes/QA -- any
    authenticated student can study any active deck, regardless of
    university or program, as long as it's the same Course.
    """

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="flashcard_decks",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="flashcard_decks",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Flashcard Deck"
        verbose_name_plural = "Flashcard Decks"

    def __str__(self):
        return f"{self.course} - {self.title}"


class Flashcard(TimeStampedModel):
    """
    A single front/back card belonging to a deck.
    """

    deck = models.ForeignKey(
        FlashcardDeck,
        on_delete=models.CASCADE,
        related_name="cards",
    )

    front = models.TextField()

    back = models.TextField()

    order = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Flashcard"
        verbose_name_plural = "Flashcards"

    def __str__(self):
        return f"{self.deck} - card #{self.pk}"


class FlashcardProgress(TimeStampedModel):
    """
    A single student's personal review progress on a single card.

    Unlike the deck/card themselves, this is NOT shared -- it's
    each student's own study progress, independent of who created
    the deck. Any authenticated student may track progress on any
    card, regardless of who owns the deck.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="flashcard_progress",
    )

    card = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name="progress_entries",
    )

    status = models.CharField(
        max_length=20,
        choices=ProgressStatus.choices,
        default=ProgressStatus.STILL_LEARNING,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "card"],
                name="unique_progress_per_user_per_card",
            )
        ]
        verbose_name = "Flashcard Progress"
        verbose_name_plural = "Flashcard Progress Entries"

    def __str__(self):
        return f"{self.user} - card #{self.card_id} - {self.status}"