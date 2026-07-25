from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.quizzes.models import (
    Quiz,
    QuizQuestion,
    QuizChoice,
    QuizAttempt,
    QuizAttemptAnswer,
)
from apps.quizzes.selectors.quiz_selector import (
    QuizSelector,
    MAX_ATTEMPTS_PER_QUIZ,
)


class QuizService:
    """
    Business logic for quizzes, questions, and attempts.
    """

    # --- Quizzes ---

    @staticmethod
    @transaction.atomic
    def create_quiz(user, **validated_data) -> Quiz:
        quiz = Quiz(creator=user, **validated_data)

        try:
            quiz.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        quiz.save()

        return quiz

    @staticmethod
    @transaction.atomic
    def update_quiz(quiz: Quiz, user, **validated_data) -> Quiz:
        QuizService._check_quiz_ownership(quiz, user)

        validated_data.pop("creator", None)

        for field, value in validated_data.items():
            setattr(quiz, field, value)

        try:
            quiz.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        quiz.save()

        return quiz

    @staticmethod
    @transaction.atomic
    def delete_quiz(quiz: Quiz, user) -> None:
        QuizService._check_quiz_ownership(quiz, user)

        quiz.delete()

    @staticmethod
    def _check_quiz_ownership(quiz: Quiz, user):
        if quiz.creator_id != user.id:
            raise PermissionDenied(
                "You can only modify quizzes you created."
            )

    # --- Questions (created/updated with their choices nested) ---

    @staticmethod
    @transaction.atomic
    def create_question(
        quiz: Quiz,
        user,
        text: str,
        order: int,
        choices: list[dict],
    ) -> QuizQuestion:
        """
        Creates a question together with all of its choices in one
        atomic call. Validated here, at creation time, rather than
        deferred to attempt-time -- so a malformed question (no
        correct choice, or fewer than 2 options) is rejected
        immediately with a clear error, not discovered later by a
        student trying to take the quiz.
        """

        QuizService._check_quiz_ownership(quiz, user)
        QuizService._validate_choices(choices)

        question = QuizQuestion(quiz=quiz, text=text, order=order)

        try:
            question.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        question.save()

        QuizService._save_choices(question, choices)

        return question

    @staticmethod
    @transaction.atomic
    def update_question(
        question: QuizQuestion,
        user,
        text: str = None,
        order: int = None,
        choices: list[dict] = None,
    ) -> QuizQuestion:
        """
        If `choices` is provided, the question's entire choice set
        is replaced atomically (delete then recreate) -- simpler
        and safer than trying to reconcile partial choice edits.
        """

        QuizService._check_quiz_ownership(question.quiz, user)

        if text is not None:
            question.text = text

        if order is not None:
            question.order = order

        try:
            question.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        question.save()

        if choices is not None:
            QuizService._validate_choices(choices)
            question.choices.all().delete()
            QuizService._save_choices(question, choices)

        return question

    @staticmethod
    @transaction.atomic
    def delete_question(question: QuizQuestion, user) -> None:
        QuizService._check_quiz_ownership(question.quiz, user)

        question.delete()

    @staticmethod
    def _validate_choices(choices: list[dict]):
        if len(choices) < 2:
            raise ValidationError(
                {"choices": "A question needs at least 2 choices."}
            )

        correct_count = sum(1 for c in choices if c.get("is_correct"))

        if correct_count != 1:
            raise ValidationError(
                {
                    "choices": (
                        "Exactly one choice must be marked correct."
                    )
                }
            )

    @staticmethod
    def _save_choices(question: QuizQuestion, choices: list[dict]):
        for index, choice_data in enumerate(choices):
            choice = QuizChoice(
                question=question,
                text=choice_data["text"],
                is_correct=choice_data.get("is_correct", False),
                order=choice_data.get("order", index),
            )

            try:
                choice.full_clean()
            except DjangoValidationError as e:
                raise ValidationError(e.message_dict)

            choice.save()

    # --- Attempts ---

    @staticmethod
    @transaction.atomic
    def submit_attempt(
        quiz: Quiz,
        user,
        answers: list[dict],
    ) -> QuizAttempt:
        """
        Submits answers for every question in a quiz in one atomic
        call (mirrors how Enrollment submits a whole semester's
        courses at once -- one validation pipeline, no partial
        submissions).

        `answers` is a list of {"question_id": int, "choice_id": int|None}.
        """

        QuizService._validate_attempt_limit(quiz, user)

        questions = list(quiz.questions.prefetch_related("choices").all())

        QuizService._validate_quiz_well_formed(questions)

        answer_map = QuizService._validate_answer_coverage(questions, answers)

        attempt = QuizAttempt(
            quiz=quiz,
            user=user,
            total_questions=len(questions),
            correct_answers=0,
        )
        attempt.save()

        correct_count = 0

        for question in questions:
            choice_id = answer_map.get(question.id)
            selected_choice = None
            is_correct = False

            if choice_id is not None:
                selected_choice = QuizService._find_choice(question, choice_id)
                is_correct = selected_choice.is_correct if selected_choice else False

            if is_correct:
                correct_count += 1

            attempt_answer = QuizAttemptAnswer(
                attempt=attempt,
                question=question,
                selected_choice=selected_choice,
                is_correct=is_correct,
            )

            try:
                attempt_answer.full_clean()
            except DjangoValidationError as e:
                raise ValidationError(e.message_dict)

            attempt_answer.save()

        attempt.correct_answers = correct_count
        attempt.save(update_fields=["correct_answers", "updated_at"])

        return attempt

    @staticmethod
    def _validate_attempt_limit(quiz: Quiz, user):
        attempts_used = QuizSelector.count_user_attempts(user, quiz)

        if attempts_used >= MAX_ATTEMPTS_PER_QUIZ:
            raise ValidationError(
                {
                    "quiz": (
                        f"You've already used all {MAX_ATTEMPTS_PER_QUIZ} "
                        "attempts for this quiz."
                    )
                }
            )

    @staticmethod
    def _validate_quiz_well_formed(questions: list[QuizQuestion]):
        if not questions:
            raise ValidationError(
                {"quiz": "This quiz has no questions yet."}
            )

        for question in questions:
            choice_list = list(question.choices.all())

            if len(choice_list) < 2:
                raise ValidationError(
                    {
                        "quiz": (
                            f"Question '{question.text[:50]}' isn't "
                            "ready to be attempted yet."
                        )
                    }
                )

            if sum(1 for c in choice_list if c.is_correct) != 1:
                raise ValidationError(
                    {
                        "quiz": (
                            f"Question '{question.text[:50]}' isn't "
                            "ready to be attempted yet."
                        )
                    }
                )

    @staticmethod
    def _validate_answer_coverage(
        questions: list[QuizQuestion],
        answers: list[dict],
    ) -> dict:
        """
        Every question in the quiz must appear exactly once in the
        submitted answers (a None choice_id means "skipped", which
        is allowed and simply scored as incorrect).
        """

        question_ids = {q.id for q in questions}
        submitted_ids = [a["question_id"] for a in answers]

        if len(submitted_ids) != len(set(submitted_ids)):
            raise ValidationError(
                {"answers": "Duplicate question_id in submission."}
            )

        submitted_id_set = set(submitted_ids)

        if submitted_id_set != question_ids:
            raise ValidationError(
                {
                    "answers": (
                        "You must submit exactly one answer for "
                        "every question in this quiz."
                    )
                }
            )

        return {a["question_id"]: a.get("choice_id") for a in answers}

    @staticmethod
    def _find_choice(question: QuizQuestion, choice_id: int):
        for choice in question.choices.all():
            if choice.id == choice_id:
                return choice

        raise ValidationError(
            {
                "answers": (
                    f"Choice {choice_id} does not belong to "
                    f"question {question.id}."
                )
            }
        )