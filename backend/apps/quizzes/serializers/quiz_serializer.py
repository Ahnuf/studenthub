from rest_framework import serializers

from apps.quizzes.models import Quiz, QuizQuestion, QuizChoice, QuizAttempt
from apps.quizzes.selectors.quiz_selector import QuizSelector
from apps.quizzes.services.quiz_service import QuizService


class QuizCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ("course", "title", "description")

    def create(self, validated_data):
        user = self.context["request"].user
        return QuizService.create_quiz(user=user, **validated_data)


class QuizListSerializer(serializers.ModelSerializer):

    course_title = serializers.CharField(source="course.title", read_only=True)
    created_by = serializers.CharField(source="creator.get_full_name", read_only=True)
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Quiz
        fields = (
            "id",
            "course",
            "course_title",
            "title",
            "description",
            "created_by",
            "question_count",
            "created_at",
        )


class QuizDetailSerializer(QuizListSerializer):
    """
    Adds the requesting user's own attempt status -- how many of
    their 5 attempts they've used, and whether they can attempt
    again. Requires `request` in context.
    """

    attempts_used = serializers.SerializerMethodField()
    attempts_remaining = serializers.SerializerMethodField()
    can_attempt = serializers.SerializerMethodField()

    class Meta(QuizListSerializer.Meta):
        fields = QuizListSerializer.Meta.fields + (
            "attempts_used",
            "attempts_remaining",
            "can_attempt",
        )

    def _attempt_status(self, obj) -> dict:
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return {"attempts_used": 0, "attempts_remaining": 0, "can_attempt": False}
        return QuizSelector.get_attempt_status(request.user, obj)

    def get_attempts_used(self, obj) -> int:
        return self._attempt_status(obj)["attempts_used"]

    def get_attempts_remaining(self, obj) -> int:
        return self._attempt_status(obj)["attempts_remaining"]

    def get_can_attempt(self, obj) -> bool:
        return self._attempt_status(obj)["can_attempt"]


class QuizUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ("title", "description")

    def update(self, instance, validated_data):
        user = self.context["request"].user
        return QuizService.update_quiz(instance, user=user, **validated_data)


# --- Choices: two different serializers on purpose ---

class QuizChoicePublicSerializer(serializers.ModelSerializer):
    """
    Used when a student is TAKING the quiz. Never includes
    is_correct -- that would hand out the answer key.
    """

    class Meta:
        model = QuizChoice
        fields = ("id", "text")


class QuizChoiceReviewSerializer(serializers.ModelSerializer):
    """
    Used only after an attempt has been submitted, for reviewing
    results -- is_correct is safe to reveal at this point.
    """

    class Meta:
        model = QuizChoice
        fields = ("id", "text", "is_correct")


class QuizChoiceInputSerializer(serializers.Serializer):
    """
    Input shape for creating/replacing a question's choices.
    """

    text = serializers.CharField(max_length=255)
    is_correct = serializers.BooleanField(default=False)
    order = serializers.IntegerField(required=False)


class QuizQuestionPublicSerializer(serializers.ModelSerializer):
    """
    What a student sees while taking the quiz -- no answer key.
    """

    choices = QuizChoicePublicSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ("id", "text", "order", "choices")


class QuizQuestionCreateSerializer(serializers.Serializer):
    text = serializers.CharField()
    order = serializers.IntegerField(default=0)
    choices = QuizChoiceInputSerializer(many=True)

    def create(self, validated_data):
        user = self.context["request"].user
        quiz = self.context["quiz"]

        return QuizService.create_question(
            quiz=quiz,
            user=user,
            text=validated_data["text"],
            order=validated_data["order"],
            choices=validated_data["choices"],
        )


class QuizQuestionUpdateSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    order = serializers.IntegerField(required=False)
    choices = QuizChoiceInputSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        user = self.context["request"].user

        return QuizService.update_question(
            instance,
            user=user,
            text=validated_data.get("text"),
            order=validated_data.get("order"),
            choices=validated_data.get("choices"),
        )


# --- Attempts ---

class AttemptAnswerInputSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    choice_id = serializers.IntegerField(required=False, allow_null=True)


class SubmitAttemptSerializer(serializers.Serializer):
    answers = AttemptAnswerInputSerializer(many=True)

    def save(self):
        request = self.context["request"]
        quiz = self.context["quiz"]

        return QuizService.submit_attempt(
            quiz=quiz,
            user=request.user,
            answers=self.validated_data["answers"],
        )


class AttemptAnswerReviewSerializer(serializers.Serializer):
    """
    Post-submission review for a single question: what was asked,
    every choice WITH is_correct revealed, and what the student
    picked.
    """

    question_id = serializers.IntegerField(source="question.id")
    question_text = serializers.CharField(source="question.text")
    choices = serializers.SerializerMethodField()
    selected_choice_id = serializers.IntegerField(
        source="selected_choice.id", allow_null=True
    )
    is_correct = serializers.BooleanField()

    def get_choices(self, obj):
        return QuizChoiceReviewSerializer(
            obj.question.choices.all(), many=True
        ).data


class QuizAttemptSerializer(serializers.ModelSerializer):

    score_percentage = serializers.FloatField(read_only=True)
    answers = AttemptAnswerReviewSerializer(many=True, read_only=True)

    class Meta:
        model = QuizAttempt
        fields = (
            "id",
            "total_questions",
            "correct_answers",
            "score_percentage",
            "answers",
            "created_at",
        )