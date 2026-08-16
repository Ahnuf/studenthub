from rest_framework import serializers

from apps.qa.models import Answer, Question
from apps.qa.services.QA_service import QAService


class QuestionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            "course",
            "title",
            "body",
        )

    def create(self, validated_data):
        user = self.context["request"].user

        return QAService.create_question(
            user=user,
            **validated_data,
        )


class QuestionListSerializer(serializers.ModelSerializer):
    """
    Lightweight representation for list views -- no body, so the
    question feed stays cheap to render.
    """

    course_title = serializers.CharField(
        source="course.title",
        read_only=True,
    )

    asked_by = serializers.CharField(
        source="asker.get_full_name",
        read_only=True,
    )

    answer_count = serializers.IntegerField(read_only=True)

    is_resolved = serializers.BooleanField(read_only=True)

    is_asker = serializers.SerializerMethodField()

    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            "id",
            "course",
            "course_title",
            "title",
            "asked_by",
            "answer_count",
            "is_resolved",
            "is_asker",
            "is_admin",
            "created_at",
        )

    def get_is_asker(self, obj) -> bool:
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return obj.asker_id == request.user.id

    def get_is_admin(self, obj) -> bool:
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return bool(request.user.is_staff)


class QuestionDetailSerializer(QuestionListSerializer):

    class Meta(QuestionListSerializer.Meta):
        fields = QuestionListSerializer.Meta.fields + ("body",)


class AnswerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ("body",)

    def create(self, validated_data):
        user = self.context["request"].user
        question = self.context["question"]

        return QAService.create_answer(
            question=question,
            user=user,
            **validated_data,
        )


class QuestionModerationSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()


class AnswerDetailSerializer(serializers.ModelSerializer):

    answered_by = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )

    vote_count = serializers.IntegerField(read_only=True)

    has_voted = serializers.SerializerMethodField()

    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = (
            "id",
            "body",
            "answered_by",
            "is_accepted",
            "vote_count",
            "has_voted",
            "is_admin",
            "created_at",
        )

    def get_has_voted(self, obj) -> bool:
        return getattr(obj, "has_voted", False)

    def get_is_admin(self, obj) -> bool:
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return bool(request.user.is_staff)


class AnswerModerationSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()