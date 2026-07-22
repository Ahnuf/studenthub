from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.assignments.models import Assignment


class AssignmentService:
    """
    Business logic for assignment operations.
    """

    @staticmethod
    @transaction.atomic
    def create_assignment(user, **validated_data) -> Assignment:
        """
        Create a new assignment owned by the given user.
        """

        assignment = Assignment(
            user=user,
            **validated_data,
        )

        try:
            assignment.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        assignment.save()

        return assignment

    @staticmethod
    @transaction.atomic
    def update_assignment(assignment: Assignment, **validated_data) -> Assignment:
        """
        Update an existing assignment.

        `user` is never accepted in validated_data -- ownership can
        never change via this method.
        """

        validated_data.pop("user", None)

        for field, value in validated_data.items():
            setattr(assignment, field, value)

        try:
            assignment.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        assignment.save()

        return assignment

    @staticmethod
    @transaction.atomic
    def delete_assignment(assignment: Assignment) -> None:
        """
        Delete an assignment.
        """

        assignment.delete()
