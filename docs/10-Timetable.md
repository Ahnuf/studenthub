# Timetable (Personal Schedule)

## Version

v1.0

Status: Design Phase

---

# Purpose

The Timetable lets a student log their own weekly class schedule
for personal reference.

Like the Assignment Tracker, this is a personal productivity
record — not an institutional timetable. It has no link to
Sections, rooms, or instructors, and does not represent the
university's official schedule.

This feature answers: "What do I have, and when, this week?"

---

# Product Philosophy Alignment

This deliberately avoids:

❌ Official class sections / room assignments

❌ Instructor-side schedule management

❌ Any dependency on a Section/ClassSession model

It only provides:

✅ A personal weekly schedule the student maintains themselves

✅ Basic conflict warnings (so a student doesn't log two
overlapping classes by mistake)

---

# Design Principles

## 1. Freeform Course Label (same as Assignments)

`course_name` is a plain string, not a foreign key to the academic
catalog — for the same reasons as the Assignment Tracker.

## 2. Weekly Recurring, Not Dated

An entry represents a recurring weekly slot ("every Monday,
10:00–11:00"), not a specific calendar date. This matches how
students actually think about "my schedule."

## 3. Student-Owned, Independent Data

Each `TimetableEntry` belongs to exactly one user, same isolation
model as `Assignment`.

## 4. No Derived Data Stored

Nothing here is calculated and stored — conflict checks run at
read/write time, not as a stored flag.

## 5. Fully Student-Controlled, Conflicts Are a Warning Only

The student sets up their timetable entirely according to their
own needs — there is no institutional validation of what's
"real." If a new or updated entry overlaps an existing one on the
same day, the system does **not** reject the request. It saves
normally and returns a warning describing the conflict, so the
student can decide for themselves whether it's intentional (e.g.
an optional session they might skip) or a mistake to fix.

---

# Proposed Model

## TimetableEntry

Fields:

- `user` — ForeignKey to User (owner)
- `course_name` — CharField, freeform
- `day_of_week` — Choice field (Monday–Sunday), stored as an
  ordered integer (0=Monday..6=Sunday) so entries sort correctly
  by day
- `start_time` — TimeField
- `end_time` — TimeField
- `location` — CharField, optional (e.g. "Room 204" or "Online")
- `created_at` / `updated_at` — standard timestamps

---

# Business Rules

- `end_time` must be after `start_time`.
- **Conflict detection (non-blocking)**: on create/update, if the
  same user already has an entry on the same `day_of_week` whose
  time range overlaps the new one, the entry still saves. The
  response includes a `warnings` list naming the conflicting
  slot's course and time, so the student is informed but never
  blocked. Overlap is checked as
  `existing.start_time < new.end_time AND new.start_time < existing.end_time`.
- No two entries need unique course names — a student may
  legitimately have a lab and a lecture for the same course on
  different days.

---

# API Endpoints

GET / POST /api/v1/timetable/

GET / PATCH / DELETE /api/v1/timetable/{id}/

---

# Architecture

Same layered flow as Assignments (doc 06 / doc 09):

Timetable API → Serializer → Service → Selector → Model → Database

---

# Responsibilities

## Selector

- `list_entries(user)` — all entries, ordered by day then time
- `get_entry(user, entry_id)` — scoped to the requesting user;
  returns `None` (→ 404) if missing or owned by someone else

## Service

- `create_entry(user, **data)` — `full_clean()` (runs both the
  time-order check and the conflict check) then save
- `update_entry(entry, **data)` — same validation path; `user`
  never client-writable
- `delete_entry(entry)`

---

# Testing Strategy

✔ Create entry (happy path)

✔ Reject `end_time <= start_time` (the one hard invariant)

✔ Overlapping entry on the same day still saves (201), with a
non-empty `warnings` list naming the conflict

✔ Overlapping entry on a *different* day saves with no warning
(no false positive)

✔ List only own entries

✔ Reject access to another user's entry by ID (404)

✔ Update an entry into a conflict with another existing entry
(should still save, with a warning, not be rejected)

---

# Out of Scope

- Institutional sections, rooms, instructor assignment
- Recurrence exceptions (e.g. "skip this one Monday")
- Calendar/timetable export (iCal, etc.) — future extension
- Notifications before class starts — future extension

---

End of Document