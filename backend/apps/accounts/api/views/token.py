from rest_framework import status
from rest_framework.views import APIView
# from apps.accounts.api.serializers import TokenRefreshSerializer
from core.api.responses import success_response


class TokenRefreshView(APIView):
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return success_response(
            message="Token refreshed successfully.",
            data=serializer.validated_data,
            status_code=status.HTTP_200_OK,
        )