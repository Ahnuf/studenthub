from django.contrib import admin

from apps.quizzes.models import (
    Quiz,
    QuizQuestion,
    QuizChoice,
    QuizAttempt,
    QuizAttemptAnswer,
)


class QuizChoiceInline(admin.TabularInline):
    model = QuizChoice
    extra = 0
    fields = ("text", "is_correct", "order")


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 0
    fields = ("text", "order")
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "title", "creator", "is_active", "created_at")
    list_filter = ("is_active", "course")
    search_fields = ("title", "description", "course__title", "creator__email")
    ordering = ("-created_at",)
    inlines = [QuizQuestionInline]


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "text", "order")
    search_fields = ("text", "quiz__title")
    ordering = ("quiz", "order")
    inlines = [QuizChoiceInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "user", "correct_answers", "total_questions", "created_at")
    search_fields = ("user__email", "quiz__title")
    ordering = ("-created_at",)


@admin.register(QuizAttemptAnswer)
class QuizAttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt", "question", "selected_choice", "is_correct")
    list_filter = ("is_correct",)