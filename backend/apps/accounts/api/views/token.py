from rest_framework.views import APIView


class TokenRefreshView(APIView):
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return success_response(
            message="Token refreshed successfully.",
            data=serializer.validated_data,
            status_code=status.HTTP_200_OK,
        )