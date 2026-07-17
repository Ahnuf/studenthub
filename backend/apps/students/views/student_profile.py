from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from apps.students.selectors.student_selector import StudentSelector
from apps.students.serializers.student_profile import (
    StudentProfileCreateSerializer,
    StudentProfileDetailSerializer,
    StudentProfileUpdateSerializer,
)


class StudentProfileAPIView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):

        if self.request.method == "POST":
            return StudentProfileCreateSerializer

        if self.request.method == "PATCH":
            return StudentProfileUpdateSerializer

        return StudentProfileDetailSerializer

    def get_profile(self):
        profile = StudentSelector.get_profile(self.request.user)

        if profile is None:
            raise NotFound("Student profile not found.")

        return profile


    def get(self, request):

        profile = self.get_profile()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        profile = serializer.save()

        return Response(
            StudentProfileDetailSerializer(profile).data,
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request):

        profile = self.get_profile()
        serializer = self.get_serializer(
            profile,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response(StudentProfileDetailSerializer(profile).data)
