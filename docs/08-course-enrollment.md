# Course Enrollment System

Version: 1.0

Sprint: 5

Status: Design Phase

---

# Purpose

The Course Enrollment System allows students to enroll in courses for an academic semester.

This module validates the student's eligibility, ensures all enrollment rules are satisfied, and creates enrollment records for each selected course.

This document defines the complete business workflow and implementation plan for the enrollment module.

---

# Objectives

The enrollment system should:

- Allow authenticated students to enroll in courses.
- Enforce university business rules.
- Prevent invalid enrollments.
- Maintain data integrity.
- Support future academic features such as GPA calculation, transcript generation, prerequisite enforcement, and graduation audits.

---

# Business Workflow

Student Login

↓

Student Dashboard

↓

Course Enrollment

↓

System Checks Eligibility

↓

Display Available Courses

↓

Student Selects Courses

↓

Validation

↓

Enrollment

↓

Confirmation

---

# Preconditions

Before enrollment begins, the following must already exist:

- User Account
- Student Profile
- University
- Program
- Academic Session
- ProgramCourse Mapping
- Course Catalog

---

# Student Journey

The student logs into StudentHub.

The student opens the Course Enrollment page.

StudentHub automatically knows:

- University
- Program
- Joined Session
- Current Semester
- Academic Status

The student should never manually select these values.

They are already stored in StudentProfile.

---

# Enrollment Request

The client submits one enrollment request containing all selected courses.

Example:

{
    "courses": [
        12,
        15,
        18,
        21,
        24
    ]
}

The semester is NOT supplied by the client.

The backend determines the semester using StudentProfile.

---

# Why One Request?

Instead of enrolling one course at a time:

POST

↓

One Course

StudentHub enrolls an entire semester in a single request.

Advantages:

- Single validation pipeline
- Atomic transaction
- Better user experience
- Prevents partial enrollments
- Easier frontend implementation

---

# Enrollment Workflow

Step 1

Authenticate User

↓

Step 2

Retrieve StudentProfile

↓

Step 3

Validate Student Eligibility

↓

Step 4

Generate Available Courses

↓

Step 5

Student Selects Courses

↓

Step 6

Validate Selection

↓

Step 7

Create StudentCourse Records

↓

Step 8

Return Success Response

---

# Student Eligibility

The student must satisfy all conditions.

Required:

Authenticated User

StudentProfile Exists

Academic Status = ACTIVE

Future Conditions:

Enrollment Window Open

Advisor Approval

Financial Clearance

Not Graduated

Not Suspended

---

# Available Courses

Initially, the system displays:

Recommended Semester Courses

+

Backlog Courses

Future versions may include:

Electives

Minor Courses

Specialization Tracks

Open Electives

---

# Validation Pipeline

Before saving any enrollment, the backend validates every rule.

---

## Authentication

User must be authenticated.

---

## Student Profile

StudentProfile must exist.

---

## Academic Status

Student must be ACTIVE.

---

## Course Validation

Every selected course must:

Belong to the student's program.

Exist in ProgramCourse.

Not be duplicated in the request.

Not already be enrolled.

Future:

Not already passed.

Prerequisites satisfied.

---

## Credit Hour Validation

Total selected credit hours must not exceed the maximum allowed.

Example:

Maximum:

18 Credits

Student selects:

4

4

3

3

3

3

↓

20 Credits

↓

Enrollment Rejected

The maximum allowed credit hours should be configurable.

---

## Duplicate Detection

The same course cannot appear twice.

Example:

{
    "courses": [
        12,
        12,
        15
    ]
}

↓

Reject Request

---

## Already Enrolled

If a StudentCourse already exists for the same course and enrollment period, enrollment should be rejected.

---

# Database Transaction

Enrollment must be atomic.

Either:

All StudentCourse records are created.

OR

None are created.

Implementation:

@transaction.atomic

---

# Data Creation

For every selected course:

Student

↓

StudentCourse

One StudentCourse record is created.

---

# Successful Response

Example

{
    "success": true,
    "message": "Courses enrolled successfully.",
    "data": {
        "courses_enrolled": 5,
        "total_credit_hours": 16
    }
}

---

# Error Responses

Validation Error

HTTP 400

Unauthorized

HTTP 401

Student Profile Missing

HTTP 404

Duplicate Enrollment

HTTP 400

Credit Limit Exceeded

HTTP 400

---

# API Endpoints

## Enroll

POST

/api/v1/students/enrollments/

---

## Current Enrollments

GET

/api/v1/students/enrollments/

---

## Enrollment Details

GET

/api/v1/students/enrollments/{id}/

---

## Drop Course

DELETE

/api/v1/students/enrollments/{id}/

---

# Architecture

Enrollment API

↓

Enrollment Serializer

↓

Enrollment Service

↓

Enrollment Selector

↓

StudentCourse

↓

Database

---

# Responsibilities

## View

Authentication

Permissions

Response

---

## Serializer

Input validation

Request parsing

Delegates business logic

---

## Service

Business rules

Enrollment workflow

Transactions

StudentCourse creation

---

## Selector

Read-only operations

Available courses

Enrollment lookups

StudentCourse queries

---

# Future Enhancements

The following features are intentionally postponed.

Prerequisite Enforcement

Advisor Approval

Enrollment Window

Elective Groups

Waitlist

Timetable Conflict Detection

Section Selection

Fee Verification

Maximum Repeat Attempts

Automatic Backlog Detection

Graduation Audit Integration

AI Course Recommendation

---

# Testing Strategy

The following scenarios must pass before completion.

Successful Enrollment

Unauthorized User

StudentProfile Missing

Inactive Student

Duplicate Course Selection

Already Enrolled

Invalid Course

Course Outside Program

Credit Limit Exceeded

Transaction Rollback

Multiple Course Enrollment

Empty Course List

---

# Sprint Deliverables

Phase 1

Business Design

✅

Phase 2

StudentCourse Review

Pending

Phase 3

Enrollment Service

Pending

Phase 4

Enrollment API

Pending

Phase 5

Testing

Pending

---

# Success Criteria

Sprint 5 is complete when:

Students can successfully enroll.

Business rules are enforced.

Transactions prevent partial enrollment.

APIs are fully tested.

Documentation is updated.

Code follows the StudentHub Backend Architecture.

---

End of Document