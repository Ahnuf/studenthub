from django.db import models



class EnrollmentStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SUBMITTED = "SUBMITTED", "Submitted"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED", "Cancelled"

class CourseStatus(models.TextChoices):
    ENROLLED = "ENROLLED", "Enrolled"
    PASSED = "PASSED", "Passed"
    FAILED = "FAILED", "Failed"
    WITHDRAWN = "WITHDRAWN", "Withdrawn"
    INCOMPLETE = "INCOMPLETE", "Incomplete"

class AcademicStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    ON_BREAK = "ON_BREAK", "On Break"
    GRADUATED = "GRADUATED", "Graduated"
    DROPPED = "DROPPED", "Dropped"