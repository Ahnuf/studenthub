from django.db.models import Count, Q

from apps.flashcards.models import (
    Flashcard,
    FlashcardDeck,
    FlashcardProgress,
    ProgressStatus,
)


class FlashcardSelector:
    """
    Read-only operations for decks, cards, and per-user progress.

    Deck/card reads are shared (not scoped to a user) -- only
    active rows are ever visible. Progress reads ARE scoped to a
    user, since that's personal study data, not shared content.
    """

    @staticmethod
    def list_decks(course_id=None, query=None):
        queryset = (
            FlashcardDeck.objects
            .select_related("course", "creator")
            .filter(is_active=True)
            .annotate(card_count=Count("cards"))
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
    def get_deck(deck_id: int):
        return (
            FlashcardDeck.objects
            .select_related("course", "creator")
            .filter(id=deck_id, is_active=True)
            .annotate(card_count=Count("cards"))
            .first()
        )

    @staticmethod
    def list_cards(deck: FlashcardDeck):
        return Flashcard.objects.filter(deck=deck)

    @staticmethod
    def get_card(deck: FlashcardDeck, card_id: int):
        return Flashcard.objects.filter(deck=deck, id=card_id).first()

    @staticmethod
    def get_card_by_id(card_id: int):
        return (
            Flashcard.objects
            .select_related("deck")
            .filter(id=card_id)
            .first()
        )

    @staticmethod
    def get_progress_map(user, deck: FlashcardDeck) -> dict:
        entries = (
            FlashcardProgress.objects
            .filter(user=user, card__deck=deck)
            .values_list("card_id", "status")
        )
        return dict(entries)

    @staticmethod
    def get_progress(user, card: Flashcard):
        return FlashcardProgress.objects.filter(user=user, card=card).first()

    @staticmethod
    def count_decks_for_courses(course_ids: list[int]) -> int:
        """
        Number of active decks available for a set of courses --
        used by the dashboard's "available decks for your courses"
        widget.
        """

        if not course_ids:
            return 0

        return (
            FlashcardDeck.objects
            .filter(is_active=True, course_id__in=course_ids)
            .count()
        )

    @staticmethod
    def get_progress_summary(user) -> dict:
        """
        Overall study progress for a user, across every deck --
        used by the dashboard, not scoped to any single course.
        """

        queryset = FlashcardProgress.objects.filter(user=user)

        total = queryset.count()
        known = queryset.filter(status=ProgressStatus.KNOWN).count()

        return {
            "cards_reviewed": total,
            "cards_known": known,
        }