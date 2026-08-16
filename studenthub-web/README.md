# StudentHub Web

Next.js (App Router, TypeScript) frontend for StudentHub.

## Setup

1. `npm install`
2. Copy `.env.local.example` to `.env.local` and point
   `NEXT_PUBLIC_API_BASE_URL` at your running Django backend
   (default assumes `http://localhost:8000/api/v1` — adjust if
   your `API_PREFIX` differs, or if the backend isn't on 8000).
3. Make sure your Django backend has CORS configured to allow
   `http://localhost:3000` (install `django-cors-headers` if you
   haven't already — it isn't in any of the apps sent so far).
4. `npm run dev` and open `http://localhost:3000`.

## What's here so far

- `/login`, `/register` — auth screens, backed by
  `lib/auth-context.tsx` (handles JWT storage + silent refresh
  via `lib/api.ts`)
- `/dashboard` — pulls `GET /students/academic-progress/` and
  renders it using the course color-coding system
  (`lib/course-colors.ts`) that will carry through every other
  screen (timetable, assignments, notes, Q&A) as they're built

## Design system

Tokens live at the top of `app/globals.css`:
- Fraunces for headings, IBM Plex Sans for body/UI, IBM Plex Mono
  for numbers (GPA, course codes, dates)
- A 6-color course palette, deterministically assigned per course
  via `courseColor()` — the same course always gets the same
  color everywhere, without needing a color field on the backend

## Not built yet

Timetable, Assignments, Notes, Course Q&A, Flashcards, Attendance
(student-facing view), and any teacher/admin screens. Auth
currently doesn't handle password reset / email verification (the
OTP endpoints) or a "profile setup" flow for a first-time student
with no `StudentProfile` yet — the dashboard will currently error
for such a user, since `/students/academic-progress/` expects one
to already exist.
