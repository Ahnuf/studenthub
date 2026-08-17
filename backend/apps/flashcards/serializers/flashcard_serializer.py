from rest_framework import serializers

from apps.flashcards.models import (
    Flashcard,
    FlashcardDeck,
    ProgressStatus,
)
from apps.flashcards.services.flashcard_service import FlashcardService


class DeckCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlashcardDeck
        fields = ("course", "title", "description")

    def create(self, validated_data):
        user = self.context["request"].user

        return FlashcardService.create_deck(
            user=user,
            **validated_data,
        )


class DeckDetailSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(
        source="course.title",
        read_only=True,
    )

    created_by = serializers.CharField(
        source="creator.get_full_name",
        read_only=True,
    )

    card_count = serializers.IntegerField(read_only=True)

    is_creator = serializers.SerializerMethodField()

    class Meta:
        model = FlashcardDeck
        fields = (
            "id",
            "course",
            "course_title",
            "title",
            "description",
            "created_by",
            "card_count",
            "is_creator",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "is_creator",
        )

    def get_is_creator(self, obj) -> bool:
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return obj.creator_id == request.user.id


class DeckUpdateSerializer(serializers.ModelSerializer):
    """
    Course is excluded because a deck stays attached to the
    course it was created under.
    """

    class Meta:
        model = FlashcardDeck
        fields = ("title", "description")

    def update(self, instance, validated_data):
        user = self.context["request"].user

        return FlashcardService.update_deck(
            instance,
            user=user,
            **validated_data,
        )


class CardCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flashcard
        fields = ("front", "back", "order")

    def create(self, validated_data):
        user = self.context["request"].user
        deck = self.context["deck"]

        return FlashcardService.create_card(
            deck,
            user=user,
            **validated_data,
        )


class CardDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    front = serializers.CharField()
    back = serializers.CharField()
    order = serializers.IntegerField()
    my_status = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_my_status(self, obj) -> str:
        progress_map = self.context.get("progress_map", {})

        return progress_map.get(
            obj.id,
            ProgressStatus.STILL_LEARNING,
        )


class CardUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flashcard
        fields = ("front", "back", "order")

    def update(self, instance, validated_data):
        user = self.context["request"].user

        return FlashcardService.update_card(
            instance,
            user=user,
            **validated_data,
        )


class ProgressSetSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=ProgressStatus.choices,
    )