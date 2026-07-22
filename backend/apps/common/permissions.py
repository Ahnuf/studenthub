from rest_framework.permissions import BasePermission

from apps.accounts.models import User


class IsStudent(BasePermission):
    """
    Allows access only to students.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.STUDENT
        )


class IsTeacher(BasePermission):
    """
    Allows access only to teachers.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.TEACHER
        )


class IsAdmin(BasePermission):
    """
    Allows access only to administrators.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )


class IsTeacherOrAdmin(BasePermission):
    """
    Allows access to teachers and administrators.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in (
                User.Role.TEACHER,
                User.Role.ADMIN,
            )
        )