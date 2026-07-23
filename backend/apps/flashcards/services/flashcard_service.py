from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.flashcards.models import Flashcard, FlashcardDeck, FlashcardProgress


class FlashcardService:
    """
    Business logic for decks, cards, and progress.
    """

    # --- Decks ---

    @staticmethod
    @transaction.atomic
    def create_deck(user, **validated_data) -> FlashcardDeck:
        deck = FlashcardDeck(creator=user, **validated_data)

        try:
            deck.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        deck.save()

        return deck

    @staticmethod
    @transaction.atomic
    def update_deck(deck: FlashcardDeck, user, **validated_data) -> FlashcardDeck:
        FlashcardService._check_deck_ownership(deck, user)

        validated_data.pop("creator", None)

        for field, value in validated_data.items():
            setattr(deck, field, value)

        try:
            deck.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        deck.save()

        return deck

    @staticmethod
    @transaction.atomic
    def delete_deck(deck: FlashcardDeck, user) -> None:
        FlashcardService._check_deck_ownership(deck, user)

        deck.delete()

    # --- Cards ---

    @staticmethod
    @transaction.atomic
    def create_card(deck: FlashcardDeck, user, **validated_data) -> Flashcard:
        """
        Only the deck's creator may add cards to it.
        """

        FlashcardService._check_deck_ownership(deck, user)

        card = Flashcard(deck=deck, **validated_data)

        try:
            card.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        card.save()

        return card

    @staticmethod
    @transaction.atomic
    def update_card(card: Flashcard, user, **validated_data) -> Flashcard:
        FlashcardService._check_deck_ownership(card.deck, user)

        for field, value in validated_data.items():
            setattr(card, field, value)

        try:
            card.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        card.save()

        return card

    @staticmethod
    @transaction.atomic
    def delete_card(card: Flashcard, user) -> None:
        FlashcardService._check_deck_ownership(card.deck, user)

        card.delete()

    @staticmethod
    def _check_deck_ownership(deck: FlashcardDeck, user):
        if deck.creator_id != user.id:
            raise PermissionDenied(
                "You can only modify decks/cards you created."
            )

    # --- Progress ---

    @staticmethod
    @transaction.atomic
    def set_progress(user, card: Flashcard, status: str) -> FlashcardProgress:
        """
        Create or update the requesting user's own progress on a
        card. Never ownership-restricted -- any authenticated user
        may track their own progress on any card, regardless of
        who created the deck.
        """

        progress, _ = FlashcardProgress.objects.get_or_create(
            user=user,
            card=card,
            defaults={"status": status},
        )

        if progress.status != status:
            progress.status = status

            try:
                progress.full_clean()
            except DjangoValidationError as e:
                raise ValidationError(e.message_dict)

            progress.save()

        return progress