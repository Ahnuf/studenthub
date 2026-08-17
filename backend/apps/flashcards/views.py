from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.throttling import ScopedRateThrottle

from apps.flashcards.selectors.flashcard_selector import FlashcardSelector
from apps.flashcards.services.flashcard_service import FlashcardService
from apps.flashcards.serializers.flashcard_serializer import (
    DeckCreateSerializer,
    DeckDetailSerializer,
    DeckUpdateSerializer,
    CardCreateSerializer,
    CardDetailSerializer,
    CardUpdateSerializer,
    ProgressSetSerializer,
)

from core.api.responses import success_response


class DeckListCreateAPIView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method == "POST":
            self.throttle_scope = "content_creation"
            return [ScopedRateThrottle()]

        return super().get_throttles()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DeckCreateSerializer

        return DeckDetailSerializer

    def get(self, request, *args, **kwargs):
        course_id = request.query_params.get("course_id")
        query = request.query_params.get("q")

        decks = FlashcardSelector.list_decks(
            course_id=course_id,
            query=query,
        )

        serializer = self.get_serializer(
            decks,
            many=True,
            context={"request": request},
        )

        return success_response(
            message="Decks fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        deck = serializer.save()

        deck = FlashcardSelector.get_deck(deck.id)

        return success_response(
            message="Deck created successfully.",
            data=DeckDetailSerializer(
                deck,
                context={"request": request},
            ).data,
            status_code=status.HTTP_201_CREATED,
        )


class DeckDetailAPIView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return DeckUpdateSerializer

        return DeckDetailSerializer

    def get_deck(self, deck_id):
        deck = FlashcardSelector.get_deck(deck_id)

        if deck is None:
            raise NotFound("Deck not found.")

        return deck

    def get(self, request, deck_id, *args, **kwargs):
        deck = self.get_deck(deck_id)

        serializer = self.get_serializer(
            deck,
            context={"request": request},
        )

        return success_response(
            message="Deck fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def patch(self, request, deck_id, *args, **kwargs):
        deck = self.get_deck(deck_id)

        serializer = self.get_serializer(
            deck,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        deck = FlashcardSelector.get_deck(deck_id)

        return success_response(
            message="Deck updated successfully.",
            data=DeckDetailSerializer(
                deck,
                context={"request": request},
            ).data,
            status_code=status.HTTP_200_OK,
        )

    def delete(self, request, deck_id, *args, **kwargs):
        deck = self.get_deck(deck_id)

        FlashcardService.delete_deck(
            deck,
            user=request.user,
        )

        return success_response(
            message="Deck deleted successfully.",
            status_code=status.HTTP_200_OK,
        )


class CardListCreateAPIView(GenericAPIView):
    """
    List cards in a deck with the requesting user's own progress,
    or create a new card.
    """

    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method == "POST":
            self.throttle_scope = "content_creation"
            return [ScopedRateThrottle()]

        return super().get_throttles()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CardCreateSerializer

        return CardDetailSerializer

    def get_deck(self, deck_id):
        deck = FlashcardSelector.get_deck(deck_id)

        if deck is None:
            raise NotFound("Deck not found.")

        return deck

    def get(self, request, deck_id, *args, **kwargs):
        deck = self.get_deck(deck_id)

        cards = FlashcardSelector.list_cards(deck)

        progress_map = FlashcardSelector.get_progress_map(
            request.user,
            deck,
        )

        serializer = CardDetailSerializer(
            cards,
            many=True,
            context={
                "progress_map": progress_map,
            },
        )

        return success_response(
            message="Cards fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request, deck_id, *args, **kwargs):
        deck = self.get_deck(deck_id)

        serializer = self.get_serializer(
            data=request.data,
            context={
                "request": request,
                "deck": deck,
            },
        )

        serializer.is_valid(raise_exception=True)

        card = serializer.save()

        progress_map = FlashcardSelector.get_progress_map(
            request.user,
            deck,
        )

        return success_response(
            message="Card created successfully.",
            data=CardDetailSerializer(
                card,
                context={
                    "progress_map": progress_map,
                },
            ).data,
            status_code=status.HTTP_201_CREATED,
        )


class CardDetailAPIView(GenericAPIView):
    """
    Update/delete a single card. Restricted to the deck creator
    by the service layer.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CardUpdateSerializer

    def get_card(self, card_id):
        card = FlashcardSelector.get_card_by_id(card_id)

        if card is None:
            raise NotFound("Card not found.")

        return card

    def patch(self, request, card_id, *args, **kwargs):
        card = self.get_card(card_id)

        serializer = self.get_serializer(
            card,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        card = serializer.save()

        progress_map = FlashcardSelector.get_progress_map(
            request.user,
            card.deck,
        )

        return success_response(
            message="Card updated successfully.",
            data=CardDetailSerializer(
                card,
                context={
                    "progress_map": progress_map,
                },
            ).data,
            status_code=status.HTTP_200_OK,
        )

    def delete(self, request, card_id, *args, **kwargs):
        card = self.get_card(card_id)

        FlashcardService.delete_card(
            card,
            user=request.user,
        )

        return success_response(
            message="Card deleted successfully.",
            status_code=status.HTTP_200_OK,
        )


class CardProgressAPIView(GenericAPIView):
    """
    Set the requesting user's own progress on a card.
    Anyone authenticated can update their own progress.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProgressSetSerializer

    def post(self, request, card_id, *args, **kwargs):
        card = FlashcardSelector.get_card_by_id(card_id)

        if card is None:
            raise NotFound("Card not found.")

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        progress = FlashcardService.set_progress(
            user=request.user,
            card=card,
            status=serializer.validated_data["status"],
        )

        return success_response(
            message="Progress updated successfully.",
            data={
                "card_id": card.id,
                "status": progress.status,
            },
            status_code=status.HTTP_200_OK,
        )