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
    user.save()

    return user