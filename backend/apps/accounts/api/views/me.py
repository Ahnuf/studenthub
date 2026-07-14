from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.api.serializers import UserSerializer
from core.api.responses import success_response



class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return success_response(
            message="User fetched successfully.",
            data=serializer.data,
        )