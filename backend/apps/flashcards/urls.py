from django.urls import path

from apps.flashcards.views import (
    DeckListCreateAPIView,
    DeckDetailAPIView,
    CardListCreateAPIView,
    CardDetailAPIView,
    CardProgressAPIView,
)

app_name = "flashcards"

urlpatterns = [
    path("decks/", DeckListCreateAPIView.as_view(), name="deck-list-create"),
    path("decks/<int:deck_id>/", DeckDetailAPIView.as_view(), name="deck-detail"),
    path("decks/<int:deck_id>/cards/", CardListCreateAPIView.as_view(), name="card-list-create"),
    path("cards/<int:card_id>/", CardDetailAPIView.as_view(), name="card-detail"),
    path("cards/<int:card_id>/progress/", CardProgressAPIView.as_view(), name="card-progress"),
]