from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


User = get_user_model()
def register_user(validated_data):
    password = validated_data.pop("password")

    validated_data.pop("password_confirm")

    user = User(**validated_data)
    user.set_password(password)
    user.full_clean()
    user.save()

    return user


def change_password(user, current_password, new_password):
    """
    Change the authenticated user's password.
    """

    if not user.check_password(current_password):
        raise ValueError("Current password is incorrect.")

    try:
        validate_password(new_password, user)
    except DjangoValidationError as e:
        raise ValueError(" ".join(e.messages))

    user.set_password(new_password)
    user.save(update_fields=["password"])

    return user