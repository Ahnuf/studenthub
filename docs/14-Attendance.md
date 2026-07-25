# Attendance

## Version

v1.0

Status: Implemented

---

# Purpose

Records daily attendance per student, per course enrollment.

**Note on scope vs. original framing:** early on, we discussed
two possible versions of attendance — a lightweight, self-tracked
personal log, versus a full institutional record marked by
teachers/admins and treated as authoritative. What got built is
the **institutional version**: attendance is marked by a
teacher/admin (never self-reported), tied to a specific
`StudentCourse` (a specific semester's enrollment, so a retake
gets independent records), and treated as the source of truth for
a student's attendance percentage. This is a deliberate departure
from the "not an ERP" philosophy in the PRD, scoped narrowly —
there's no scheduling/section/timetable infrastructure behind it,
just recording and summarizing.

---

# Design Principles

## 1. Marked, Not Self-Reported

`AttendanceRecord.marked_by` is always a teacher/admin
(`IsTeacherOrAdmin` permission on the marking endpoints). A
student can view their own records but never create or edit them.

## 2. One Record Per Student-Course Per Day

Unique constraint on (`student_course`, `date`). Re-marking a day
(correcting a mistake) overwrites the existing record rather than
erroring or creating a duplicate.

## 3. Leave Is Excluded From the Percentage

`LEAVE` (excused absence) doesn't count against the student the
way `ABSENT` does — the percentage denominator is
`present + absent` only; `total_sessions` still includes leave for
transparency, but the percentage itself doesn't penalize an
excused day.

---

# Model

## AttendanceRecord

- `student_course` — FK to `StudentCourse` (not `ProgramCourse` —
  ties attendance to a specific semester's enrollment)
- `date`
- `status` (`PRESENT` / `ABSENT` / `LEAVE`)
- `marked_by` — FK to User, nullable (`SET_NULL` if the marking
  user's account is later removed)
- `remarks`

---

# Business Rules

- `date` cannot be in the future (validated in `clean()`).
- Only a teacher/admin may mark attendance (single or bulk).
- A student may view only their own attendance; teachers/admins
  may view any student's.

---

# API Endpoints

POST `/attendance/mark/` — mark one student, one day

POST `/attendance/bulk-mark/` — mark a whole class session at once

GET `/attendance/roster/` — the `StudentCourse` roster for a given
`program_course_id` + `academic_session_id`, so a teacher can build
the bulk-mark payload without already knowing every `StudentCourse` ID

GET `/attendance/{student_course_id}/` — summary + day-by-day
records for one student's course enrollment

---

# Dashboard Integration

Surfaced on the Academic Progress Dashboard as a read-only
widget — overall percentage across the student's current courses,
a per-course breakdown, and an `at_risk_courses` list (below 75%,
a common institutional eligibility threshold, adjustable). The
dashboard only displays this; there's no student-facing action
tied to it, unlike the other widgets.

---

# Known Issue (Documented, Not Yet Fixed)

`AttendanceRosterAPIView` currently returns its "required
parameters missing" `400` case using `success_response` instead of
`error_response` — meaning the JSON body says `"success": true`
while the HTTP status says `400`. Should be switched to
`error_response` (or a raised `ValidationError`) to match how the
rest of the codebase handles validation failures.

---

# Out of Scope (v1)

- Attendance-based enrollment/exam blocking (currently just
  surfaced as a dashboard warning, not enforced anywhere)
- Timetable/section-based session scheduling
- Student self-check-in

---

End of Document