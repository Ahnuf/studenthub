from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from django.db import transaction
from apps.students.models import StudentProfile
from apps.students.selectors.student_selector import StudentSelector


User = get_user_model()

class StudentService:
    """
    Business logic for student operations.
    """

    @staticmethod
    @transaction.atomic
    def create_profile(user: User, **validated_data) -> StudentProfile:
        """
        Create a student profile for a user.
        """

        if StudentSelector.profile_exists(user):
            raise ValidationError(
                "Student profile already exists."
            )

        profile = StudentProfile(
            user=user,
            **validated_data,
        )

        try:
            profile.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        profile.save()

        return profile

    @staticmethod
    @transaction.atomic
    def update_profile(
        profile: StudentProfile,
        **validated_data,
    ) -> StudentProfile:
        """
        Update an existing student profile.
        """

        for field, value in validated_data.items():
            setattr(profile, field, value)

        try:
            profile.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        profile.save()
        return profile