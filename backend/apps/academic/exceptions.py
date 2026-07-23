class AcademicException(Exception):
    """
    Base exception for the Academic app.
    """


class GradingSchemeNotFound(AcademicException):
    """
    Raised when an active grading scheme cannot be found.
    """


class GradePointNotFound(AcademicException):
    """
    Raised when no grade point matches the given marks.
    """