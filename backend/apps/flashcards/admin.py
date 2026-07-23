from django.contrib import admin

from apps.flashcards.models import Flashcard, FlashcardDeck, FlashcardProgress


class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 0
    fields = ("front", "back", "order")


@admin.register(FlashcardDeck)
class FlashcardDeckAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "title", "creator", "is_active", "created_at")
    list_filter = ("is_active", "course")
    search_fields = ("title", "description", "course__title", "creator__email")
    ordering = ("-created_at",)
    inlines = [FlashcardInline]


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ("id", "deck", "front", "order", "created_at")
    search_fields = ("front", "back", "deck__title")
    ordering = ("deck", "order")


@admin.register(FlashcardProgress)
class FlashcardProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "card", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("user__email",)