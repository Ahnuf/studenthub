# Assignment Tracker

## Version

v1.0

Status: Design Phase

---

# Purpose

The Assignment Tracker lets a student log their own assignments,
deadlines, and progress in one place.

It is a personal productivity tool, not a submission or grading
system. StudentHub does not receive, store, or grade any actual
coursework — the student's real assignments continue to live
wherever their university actually runs them (Google Classroom,
LMS, in-class handouts, etc.).

This feature answers one question for the student:

"What do I need to submit, and when?"

---

# Product Philosophy Alignment

Per the PRD (doc 01), StudentHub is an academic workspace, not an
ERP or LMS replacement.

This feature deliberately avoids:

❌ Teacher-side assignment creation

❌ File submission to a teacher

❌ Grading or feedback

❌ Any link to official coursework platforms

It only provides:

✅ A personal deadline list

✅ Manual status tracking

✅ Dashboard visibility into what's due soon

---

# Design Principles

## 1. Freeform, Not Catalog-Linked

An assignment belongs to a course *label*, not a `StudentCourse`
or `ProgramCourse` record.

Reasoning:

The academic catalog (`ProgramCourse`) represents the official
curriculum. It has no relationship to where day-to-day coursework
actually happens. Forcing a catalog link would block a student
from logging an assignment unless it matched the catalog exactly.

Example:

course_name = "Database Systems"

Not a foreign key. Just a string the student types.

---

## 2. Student-Owned, Independent Data

Like `StudentCourse`, every `Assignment` belongs to exactly one
student (via their `User`). Two students see completely different
assignment lists, even if they're in the same program.

---

## 3. No Derived Data Stored

Anything calculable (e.g. "3 assignments due this week", "2
overdue") is calculated at read time from raw `Assignment` rows —
never stored.

---

# Proposed Model

## Assignment

Fields:

- `user` — ForeignKey to the User (owner)
- `course_name` — CharField, freeform (e.g. "Database Systems")
- `title` — CharField (e.g. "Assignment 2 — Normalization")
- `description` — TextField, optional
- `due_date` — DateField
- `status` — CharField, choices:
  - `PENDING`
  - `IN_PROGRESS`
  - `COMPLETED`
- `created_at` / `updated_at` — standard timestamps

Not included in v1 (future extension):

- Attachment / file upload
- Priority level
- Reminder / notification scheduling
- Link to `StudentCourse` (optional, non-blocking)

---

# Business Rules

- `due_date` has no restriction relative to today — a student may
  log a past-due assignment (e.g. to record it was missed) or a
  future one.
- `status` defaults to `PENDING` on creation.
- No two assignments need to be unique — a student may reasonably
  have two different assignments with the same title/course
  (e.g. recurring weekly labs), so no uniqueness constraint is
  enforced.
- Only the owning student can view, update, or delete their own
  assignments.

---

# API Endpoints

## List / Create

GET /api/v1/students/assignments/

POST /api/v1/students/assignments/

---

## Retrieve / Update / Delete

GET /api/v1/students/assignments/{id}/

PATCH /api/v1/students/assignments/{id}/

DELETE /api/v1/students/assignments/{id}/

---

# Architecture

Assignment API

↓

Assignment Serializer

↓

Assignment Service

↓

Assignment Selector

↓

Assignment Model

↓

Database

Follows the same layered architecture as the rest of the backend
(doc 06) — no exceptions for this feature.

---

# Responsibilities

## View

Authentication (`IsAuthenticated`)

Ownership enforcement (a student can only ever act on their own
`Assignment` rows — enforced at the selector/service layer, not
just relying on serializer input)

Response formatting

---

## Serializer

Input validation (title required, due_date required and valid,
status must be one of the defined choices)

Output shape

---

## Service

Create / update / delete operations

Enforces the "no changing ownership" rule (user field is never
client-writable)

---

## Selector

`list_assignments(user)` — all assignments for a user, ordered by
due_date

`list_upcoming(user)` — assignments due in the next N days,
excluding COMPLETED

`get_assignment(user, assignment_id)` — single assignment, scoped
to the requesting user (returns None / raises NotFound if it
belongs to someone else — this must never leak another student's
assignment by ID)

---

# Dashboard Integration

A lightweight "Assignments Due Soon" widget can be added to the
Academic Progress Dashboard (doc 04) once this feature exists:

- Assignments due in the next 7 days
- Overdue assignments (`due_date` < today AND status != COMPLETED)

This is additive — it does not require changes to the existing
dashboard sections already built.

---

# Testing Strategy

✔ Create assignment (happy path)

✔ List own assignments only (never another user's)

✔ Update status

✔ Delete assignment

✔ Reject request for another user's assignment by ID (404, not
403 — avoid confirming the ID exists)

✔ Validation: missing title, missing due_date, invalid status

✔ Unauthorized (no token)

---

# Future Extensions

- File attachment (assignment brief / instructions)
- Priority / urgency flagging
- Reminder notifications (push / email) as due date approaches
- Optional link to `StudentCourse` for students who want tighter
  integration
- Recurring assignments (e.g. weekly lab reports)

---

# Out of Scope

- Teacher-created assignments
- Submission of completed work
- Grading or feedback
- Integration with Google Classroom / Moodle / any external LMS

---

End of Document