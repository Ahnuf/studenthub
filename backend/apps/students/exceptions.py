class StudentException(Exception):
    """
    Base exception for the Students app.
    """


class EnrollmentNotFound(StudentException):
    """
    Raised when an enrollment cannot be found.
    """


class StudentCourseNotFound(StudentException):
    """
    Raised when a student course cannot be found.
    """