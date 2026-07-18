# Grading Policy System

## Version

v1.0

---

# Purpose

The Grading Policy System defines how academic grades are interpreted for different universities.

It acts as the single source of truth for:

- Grade Points
- GPA Calculation
- Passing Grades
- Percentage Ranges
- Academic Standing

StudentCourse stores only the student's academic result.

The grading policy determines how that result is evaluated.

---

# Design Principles

## 1. Universities Own Their Grading Policies

Each university may have its own grading system.

StudentHub must never assume that all universities follow the same grading scale.

Example:

FAST

A = 4.00

Another University

A = 3.75

---

## 2. Never Store Derived GPA Values

StudentCourse stores:

- Grade
- Marks

Never:

- Grade Points
- GPA

These values should always be calculated using the university's grading policy.

---

## 3. One Active Policy Per University

Each university may have multiple grading policies over time.

Only one policy should be active at any given moment.

Example:

FAST Undergraduate (2022)

FAST Undergraduate (2026)

FAST Graduate

---

# Proposed Models

## GradingPolicy

Purpose:

Represents one grading policy used by a university.

Fields:

- University
- Name
- Description
- Effective From
- Effective Until
- Is Active

Example:

FAST Undergraduate 2026

---

## GradeRule

Purpose:

Defines how a single grade is interpreted.

Relationship:

GradingPolicy

↓

GradeRule

Fields:

- Grade
- Minimum Percentage
- Maximum Percentage
- Grade Point
- Is Passing

Example:

Grade

A

Minimum Percentage

85

Maximum Percentage

100

Grade Point

4.00

Passing

Yes

---

# Data Flow

StudentCourse

↓

Grade

↓

Grading Policy

↓

Grade Point

↓

Academic Progress Service

↓

CGPA

---

# Responsibilities

StudentCourse

Stores:

- Grade
- Marks

Does NOT calculate:

- GPA
- Grade Points

---

GradingPolicy

Responsible for:

- Grade Mapping
- Grade Points
- Pass / Fail Rules

---

AcademicProgressService

Responsible for:

- SGPA
- CGPA
- Academic Standing
- Degree Progress

---

# Example Workflow

Student receives:

Grade = B+

↓

AcademicProgressService

↓

Load University's Active Grading Policy

↓

Find GradeRule

↓

Grade Point = 3.33

↓

Calculate GPA

---

# Future APIs

GET

/api/v1/grading-policy/

Returns:

Current grading policy for a university.

---

GET

/api/v1/grading-policy/grades/

Returns:

All grade rules.

---

# Future Services

GradingPolicyService

Responsibilities:

- Convert Grade → Grade Points
- Convert Marks → Grade
- Determine Pass / Fail
- Validate Grade Ranges

---

AcademicProgressService

Uses:

GradingPolicyService

to calculate:

- SGPA
- CGPA
- Academic Standing
- Graduation Eligibility

---

# Future Features

Multiple grading systems per university

Historical grading policies

Department-specific grading policies

Graduate and Undergraduate policies

Custom grading scales

Letter-grade conversion

Percentage conversion

Transcript generation

---

# Engineering Principles

StudentCourse owns academic results.

GradingPolicy owns academic interpretation.

AcademicProgressService owns academic calculations.

Never duplicate grading logic.

Never hardcode grade points.

Always resolve grade points through the active grading policy.

---

# Future Integration

StudentProfile

↓

StudentCourse

↓

Grade

↓

GradingPolicy

↓

AcademicProgressService

↓

Academic Progress Dashboard

↓

AI Academic Advisor