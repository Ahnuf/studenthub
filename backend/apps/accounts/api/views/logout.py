from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return success_response(
            message="Logged out successfully."
        )