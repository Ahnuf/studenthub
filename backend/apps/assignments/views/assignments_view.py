from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.assignments.selectors.assignments_selector import AssignmentSelector
from apps.assignments.services.assignments_service import AssignmentService
from apps.assignments.serializers.assignments_serializer import (
    AssignmentCreateSerializer,
    AssignmentDetailSerializer,
    AssignmentUpdateSerializer,
)
from core.api.responses import success_response


class AssignmentListCreateAPIView(GenericAPIView):
    """
    List the authenticated user's assignments, or create a new one.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AssignmentCreateSerializer

        return AssignmentDetailSerializer

    def get(self, request, *args, **kwargs):
        assignments = AssignmentSelector.list_assignments(request.user)

        serializer = self.get_serializer(assignments, many=True)

        return success_response(
            message="Assignments fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        assignment = serializer.save()

        return success_response(
            message="Assignment created successfully.",
            data=AssignmentDetailSerializer(assignment).data,
            status_code=status.HTTP_201_CREATED,
        )


class AssignmentDetailAPIView(GenericAPIView):
    """
    Retrieve, update, or delete a single assignment.

    Always scoped to the requesting user -- an assignment
    belonging to another user returns 404, never 403, so the
    existence of the ID is never confirmed to a non-owner.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return AssignmentUpdateSerializer

        return AssignmentDetailSerializer

    def get_assignment(self, request, assignment_id):
        assignment = AssignmentSelector.get_assignment(
            user=request.user,
            assignment_id=assignment_id,
        )

        if assignment is None:
            raise NotFound("Assignment not found.")

        return assignment

    def get(self, request, assignment_id, *args, **kwargs):
        assignment = self.get_assignment(request, assignment_id)

        serializer = self.get_serializer(assignment)

        return success_response(
            message="Assignment fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def patch(self, request, assignment_id, *args, **kwargs):
        assignment = self.get_assignment(request, assignment_id)

        serializer = self.get_serializer(
            assignment,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        assignment = serializer.save()

        return success_response(
            message="Assignment updated successfully.",
            data=AssignmentDetailSerializer(assignment).data,
            status_code=status.HTTP_200_OK,
        )

    def delete(self, request, assignment_id, *args, **kwargs):
        assignment = self.get_assignment(request, assignment_id)

        AssignmentService.delete_assignment(assignment)

        return success_response(
            message="Assignment deleted successfully.",
            status_code=status.HTTP_200_OK,
        )
