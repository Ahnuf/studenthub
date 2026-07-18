# Academic Progress Dashboard

## Version

v1.0

---

# Purpose

The Academic Progress Dashboard is the primary screen students interact with after completing onboarding.

Unlike traditional university portals, StudentHub should not only display academic information but also analyze it and provide actionable insights.

The dashboard must answer questions such as:

- Where am I academically?
- How much of my degree have I completed?
- Which courses are remaining?
- Do I have any backlogs?
- Am I on track for graduation?
- What should I do next?

---

# Design Principles

The dashboard follows three core principles.

## 1. Never Store Calculated Data

Only store raw academic records.

Everything else should be calculated.

Examples:

❌ CGPA

❌ Completed Credits

❌ Degree Progress

❌ Remaining Credits

❌ Backlog Count

Instead:

Calculate them from StudentCourse and ProgramCourse.

---

## 2. Academic Catalog is the Source of Truth

The official curriculum always comes from:

University

↓

Program

↓

ProgramCourse

Students cannot modify the academic catalog.

---

## 3. Student Data is Personal

StudentProfile and StudentCourse represent a student's own academic journey.

Two students in the same program may have completely different dashboards.

---

# Dashboard Sections

## Section 1 — Academic Identity

Purpose:

Shows who the student is academically.

Source:

StudentProfile

Widgets:

- University
- Program
- Current Semester
- Joined Session
- Academic Status
- Expected Graduation Year

Stored:

Yes

---

## Section 2 — Current Semester

Purpose:

Shows the student's current workload.

Source:

StudentCourse

Widgets:

- Current Courses
- Current Credit Hours
- Semester GPA

Stored:

No

Calculated:

Yes

---

## Section 3 — Degree Progress

Purpose:

Shows degree completion.

Source:

ProgramCourse

StudentCourse

Widgets:

- Completed Credits
- Remaining Credits
- Completed Courses
- Remaining Courses
- Degree Progress %

Stored:

No

Calculated:

Yes

---

## Section 4 — Academic Performance

Purpose:

Displays performance.

Source:

StudentCourse

Widgets:

- CGPA
- SGPA
- Passed Courses
- Failed Courses
- Backlogs
- Retaken Courses

Stored:

No

Calculated:

Yes

---

## Section 5 — Curriculum Progress

Purpose:

Tracks progress by course category.

Source:

ProgramCourse

StudentCourse

Widgets:

Core Courses

Electives

University Requirements

General Education

Example:

Core Courses

18 / 24

Electives

7 / 12

Stored:

No

Calculated:

Yes

---

## Section 6 — Graduation Audit

Purpose:

Checks graduation eligibility.

Source:

ProgramCourse

StudentCourse

Widgets:

Graduation Eligible

Remaining Credits

Missing Core Courses

Missing Electives

Missing University Requirements

Stored:

No

Calculated:

Yes

---

## Section 7 — Academic Timeline

Purpose:

Displays semester-by-semester progress.

Source:

StudentCourse

Widgets:

Semester 1

Semester 2

Semester 3

Semester 4

Semester 5 (Backlogs)

Semester 6

Semester 7 (Current)

Stored:

No

Calculated:

Yes

---

## Section 8 — AI Academic Advisor (Future)

Purpose:

Provide personalized academic guidance.

Examples:

• You currently have two backlog courses.

• Completing both this semester keeps you on track for graduation.

• Your workload is heavier than average.

• Consider taking one elective instead of two.

• Based on your performance, you are projected to graduate in Spring 2030.

Stored:

No

Generated dynamically.

---

# Data Ownership

StudentProfile

Responsible for:

- Academic Identity

StudentCourse

Responsible for:

- Course Enrollment
- Grades
- Results

ProgramCourse

Responsible for:

- Official Curriculum

AcademicSession

Responsible for:

- Academic Timeline

---

# Service Layer

Dashboard calculations should never live inside models.

Instead:

AcademicProgressService

Responsibilities:

- Calculate CGPA
- Calculate SGPA
- Calculate Degree Progress
- Calculate Completed Credits
- Calculate Remaining Credits
- Detect Backlogs
- Graduation Audit
- AI Insights

Example

AcademicProgressService(student).build_dashboard()

---

# MVP Dashboard

The initial release should include:

✅ Academic Identity

✅ Current Courses

✅ Completed Credits

✅ Remaining Credits

✅ Degree Progress

✅ CGPA

✅ Current Semester GPA

✅ Expected Graduation

---

# Phase 2

Add:

- Backlog Detection
- Graduation Audit
- Academic Timeline
- Category Progress

---

# Phase 3

Add:

- AI Academic Advisor
- Workload Analysis
- Graduation Prediction
- Personalized Semester Planning
- What-if GPA Calculator

---

# Engineering Principles

Always calculate derived values.

Never duplicate academic data.

Keep dashboard logic inside services.

Academic Catalog remains immutable.

Student data remains independent.

Dashboard should explain progress, not simply display numbers.