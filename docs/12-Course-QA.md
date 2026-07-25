# Course Q&A

## Version

v1.0

Status: Implemented

---

# Purpose

The free, human-powered alternative to an AI Tutor chatbot. A
student posts a question about a course; any other authenticated
student can answer it. Costs nothing to run (no LLM calls), and
the value compounds over time — an answered question helps every
future student who has the same one, unlike a private chatbot
conversation.

---

# Design Principles

## 1. Platform-Wide Visibility, Same as Notes

`course` is a ForeignKey to `Course` (the university-agnostic
catalog entry), not `ProgramCourse`. A student in one program can
see and answer a question posted by a student in a completely
different program, as long as it's the same underlying course.

## 2. Shared Content, Personal Ownership for Writes

Anyone can read/list/search questions and answers. Only the
original asker can edit/delete their question or mark an answer
accepted; only an answer's author can edit/delete it. Since the
content is already public via search, a non-owner attempting to
modify it gets `403`, not `404` — there's nothing to hide the
existence of.

## 3. Accepted Answer via Boolean + DB Constraint, Not a Circular FK

The original design considered a nullable `Question.accepted_answer`
FK pointing to `Answer`. The implemented version instead puts
`is_accepted` directly on `Answer`, with a partial unique
constraint (`condition=Q(is_accepted=True)`) ensuring at most one
accepted answer per question at the database level. This avoids
the circular-FK dance (`Question` → `Answer` → `Question`) that
the original design would have needed and can never end up in an
inconsistent state even from a bug elsewhere in the code.

## 4. Upvotes Are Rows, Not a Counter

`AnswerVote` existing for a (user, answer) pair *is* the vote —
there's no direction/value, just present or absent, enforced by a
unique constraint. A raw counter field on `Answer` couldn't
prevent double-voting on its own; the vote table can.

---

# Models

## Question

- `user` — the asker
- `course` — FK to `Course`
- `title`, `body`
- `created_at` / `updated_at`

## Answer

- `question` — FK to `Question`
- `user` — the answerer
- `body`
- `is_accepted` — boolean, DB-constrained to at most one `True`
  per question

## AnswerVote

- `answer`, `user` — unique together (one vote per user per answer)

---

# Business Rules

- A user cannot answer their own question (validated in
  `Answer.clean()`).
- Only the original asker may mark an answer as accepted.
- Any authenticated user may post an answer to any question.
- Non-owner edit/delete attempts on a question or answer → `403`.

---

# API Endpoints

GET / POST `/questions/` — list (filterable by `course_id`) / post
a question

GET `/questions/{id}/` — question + its answers together

POST `/questions/{id}/answers/` — post an answer

POST `/answers/{id}/accept/` — asker marks an answer accepted

POST `/answers/{id}/upvote/` — toggle the requesting user's upvote

---

# Known Gaps (Documented, Not Yet Addressed)

- **Self-upvoting is not currently blocked.** A user can upvote
  their own answer to inflate its rank. Worth adding a guard in
  the vote service if this becomes a real problem in practice.
- **No moderation/reporting mechanism**, and no `is_active` flag
  on `Question`/`Answer` (unlike `Note`, which has one). If
  moderation becomes necessary, it needs to be added from scratch
  here rather than just flipped on.

---

# Out of Scope (v1)

- Reporting, flagging, or approval workflows
- Comment threads on answers (flat list only)
- Teacher-specific answering privileges (any authenticated user
  can answer, regardless of role)

---

End of Document