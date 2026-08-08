from django.contrib import admin

from apps.qa.models import Question, Answer, AnswerVote


class AnswerInline(admin.TabularInline):
    model = Answer
    fk_name = "question"
    extra = 0
    fields = ("user", "body", "is_accepted", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course",
        "title",
        "asker",
        "is_resolved",
        "created_at",
    )
    list_filter = (
        "course",
    )
    search_fields = (
        "title",
        "body",
        "course__title",
        "user__email",
    )
    ordering = ("-created_at",)
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "user",
        "is_accepted",
        "upvote_count",
        "created_at",
    )
    list_filter = (
        "is_accepted",
    )
    search_fields = (
        "body",
        "user__email",
        "question__title",
    )
    ordering = ("-created_at",)

    def upvote_count(self, obj):
        return obj.votes.count()

    upvote_count.short_description = "Upvotes"


@admin.register(AnswerVote)
class AnswerVoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "answer",
        "user",
        "created_at",
    )
    search_fields = (
        "user__email",
    )
    ordering = ("-created_at",)