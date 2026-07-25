# Flashcards

## Version

v1.0

Status: Implemented

---

# Purpose

A manual, zero-cost self-study tool. A student creates a deck of
front/back cards for a course; any student can study any deck,
tracking their own personal progress independently of who created
it. Built as the free alternative to AI-generated flashcards,
with an intentional upgrade path: once there's budget for an LLM,
"auto-generate a deck from a Note" can sit on top of this same
data model without changing it.

---

# Design Principles

## 1. Shared Content, Personal Progress

Decks and cards follow the same visibility model as Notes/QA —
shared platform-wide, creator-owned for edits. Progress is the
opposite: strictly personal, one row per (user, card), and never
gated by who created the deck. Studying someone else's shared
deck is the entire point, so marking your own progress on their
cards is always allowed.

## 2. No Spaced Repetition Algorithm (Yet)

Progress is a simple two-state toggle (`STILL_LEARNING` / `KNOWN`),
not a full spaced-repetition scheduler (e.g. SM-2/Anki-style
intervals). That's a reasonable v2 addition on top of the same
`FlashcardProgress` table, not a redesign.

---

# Models

## FlashcardDeck

- `creator`, `course`, `title`, `description`, `is_active`

## Flashcard

- `deck`, `front`, `back`, `order`

## FlashcardProgress

- `user`, `card`, `status` (`STILL_LEARNING` / `KNOWN`) — unique
  per (user, card)

---

# Business Rules

- Only a deck's creator may add/edit/delete its cards or the deck
  itself; non-owner attempts → `403`.
- Any authenticated user may set their own progress on any card,
  regardless of who created its deck.
- A card's `my_status` is looked up per-request from a
  `{card_id: status}` map built in one query, rather than N+1
  queries per card when listing a deck.

---

# API Endpoints

GET / POST `/decks/` — browse/search / create

GET / PATCH / DELETE `/decks/{id}/` — creator-only writes

GET / POST `/decks/{id}/cards/` — list (with your progress per
card) / add a card (creator-only)

PATCH / DELETE `/cards/{id}/` — creator-only

POST `/cards/{id}/progress/` — set your own progress (open to
anyone)

---

# Out of Scope (v1)

- AI-generated cards (budget-blocked; same upgrade path noted
  above)
- Spaced repetition scheduling
- Deck ratings or upvotes

---

End of Document