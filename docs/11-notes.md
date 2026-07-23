# Notes (Shared, Searchable)

## Version

v1.0

Status: Design Phase

---

# Purpose

Lets a student upload notes (a file plus a heading/sub-heading)
against a course. Unlike Assignments and Timetable, notes are
**shared**: any student searching for a course can find and view
notes uploaded by any other student, regardless of university or
program, as long as it's the same underlying `Course`.

This answers: "Does anyone already have notes on this topic?"

---

# Why This Is Different From Assignments / Timetable

Those features are strictly personal — a student can only ever
see their own data. Notes deliberately breaks that isolation:
upload is personal (one uploader), but visibility is shared
(every student can read).

This has real consequences:

- **Catalog-linked, not freeform.** A note links to the actual
  `Course` model, not a typed label. This is what makes cross-
  program, cross-university search actually work — `Course.title`
  is unique platform-wide, so "Database Systems" is the same row
  no matter who teaches it, which is exactly what makes it
  possible for a student in one program to find notes uploaded by
  a student in a completely different program.
- **Different permission model.** Reading is open to any
  authenticated student. Editing/deleting is restricted to the
  uploader. Because existence is already public (visible via
  search), a non-owner attempting to modify a note gets `403`,
  not `404` — unlike Assignments/Timetable, where `404` is used
  specifically to avoid confirming a private resource exists.

---

# Design Principles

## 1. Course-Linked, Platform-Wide Visibility

`course` is a ForeignKey to `Course` (the university-agnostic
catalog entry), not `ProgramCourse` and not freeform text.
Visibility is intentionally platform-wide — any student, any
university, any program.

## 2. Upload Is Personal, Content Is Shared

`uploader` (the User who uploaded it) is tracked for permissions
and attribution, but every other authenticated student can view,
list, and search all active notes.

## 3. Open Uploads in v1, Governance Deferred

No approval workflow and no reporting mechanism in v1. An
`is_active` flag (same pattern as `University`/`Program`/`Course`)
lets an admin hide a note later without deleting it, keeping the
door open for moderation without building it now.

---

# Proposed Model

## Note

Fields:

- `uploader` — ForeignKey to User (who uploaded it)
- `course` — ForeignKey to `Course` (academic.Course, not
  ProgramCourse)
- `main_heading` — CharField
- `sub_heading` — CharField, optional
- `description` — TextField, optional (short context about the note)
- `file` — FileField, the actual uploaded content
- `is_active` — BooleanField, default True (governance lever)
- `created_at` / `updated_at`

Allowed file types (v1 assumption, adjustable): PDF, DOC/DOCX,
PPT/PPTX, JPG/JPEG, PNG.

Max file size (v1 assumption): 20MB.

---

# Business Rules

- Any authenticated user can list/search/view any active note.
- Only the uploader can update or delete their own note.
- A non-owner attempting to update/delete gets `403` (existence
  is already public via search — this is a permission failure,
  not a privacy one).
- File extension and size are validated on upload.
- No uniqueness constraint — the same student may upload multiple
  notes for the same course (e.g. per chapter/topic), and
  different students may upload notes for the same course too.

---

# API Endpoints

## List / Search / Upload

GET /api/v1/notes/?course_id={id}

GET /api/v1/notes/?q={search text}

POST /api/v1/notes/

`q` matches against `main_heading`, `sub_heading`, and the
related course's `title`.

---

## Retrieve / Update / Delete

GET /api/v1/notes/{id}/ — any authenticated user

PATCH /api/v1/notes/{id}/ — uploader only (403 otherwise)

DELETE /api/v1/notes/{id}/ — uploader only (403 otherwise)

---

# Architecture

Note API → Serializer → Service → Selector → Model → Database

Same layered flow as every other feature (doc 06).

---

# Responsibilities

## Selector

- `list_notes(course_id=None, query=None)` — active notes only,
  optionally filtered by course and/or search text, newest first
- `get_note(note_id)` — a single active note, visible to anyone;
  `None` (→ 404) if missing or inactive
- `list_my_notes(user)` — notes uploaded by the requesting user
  (for a "my uploads" view)

## Service

- `create_note(user, **data)` — `full_clean()` then save
- `update_note(note, user, **data)` — raises `PermissionDenied`
  (403) if `note.uploader != user`, otherwise `full_clean()` +
  save
- `delete_note(note, user)` — same ownership check, then delete

---

# Testing Strategy

✔ Upload a note (happy path)

✔ Reject disallowed file extension

✔ Reject oversized file

✔ Any authenticated user can view/list/search notes uploaded by
someone else, across programs/universities

✔ Non-owner attempting update/delete → 403

✔ Owner can update/delete their own note

✔ Search matches on heading, sub-heading, and course title

✔ Inactive notes excluded from list/search/detail

---

# Out of Scope (v1)

- Reporting / flagging / approval workflow
- Rich text note content typed directly on the platform (this
  version is file-upload only)
- Note ratings / upvotes
- AI summarization of uploaded notes (see the separate note on
  future AI features)

---

End of Document
