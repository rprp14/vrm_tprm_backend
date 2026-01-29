from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Assessment
from .serializers import AssessmentSerializer

from apps.workflow.engine import validate_transition
from apps.workflow.exceptions import WorkflowForbidden, WorkflowConflict
from apps.audit.services import log_audit_event
class AssessmentViewSet(viewsets.ModelViewSet):
    """
    Assessment workflow API
    Roles:
    - Admin   : create assessment, send for review
    - Vendor  : submit assessment
    - Reviewer: approve / reject assessment
    """

    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Users can see only assessments of their own org
        return Assessment.objects.filter(org_id=self.request.user.org_id)
    def perform_create(self, serializer):
        if self.request.user.role != "Admin":
            raise PermissionDenied("Only Admin can create assessments")

        serializer.save(org_id=self.request.user.org_id)

        log_audit_event(
            user_id=self.request.user.id,
            action="create_assessment",
            entity="assessment",
            entity_id=None,
            org_id=self.request.user.org_id
        )
    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        assessment = self.get_object()

        try:
            validate_transition(
                entity="assessment",
                action="submit",
                current_status=assessment.status,
                role=request.user.role,
                context={
                    "assessment_status": assessment.status,
                    "org_id": assessment.org_id,
                    "user_org": request.user.org_id,
                }
            )
        except WorkflowForbidden as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except WorkflowConflict as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

        assessment.status = "submitted"
        assessment.save(update_fields=["status"])

        log_audit_event(
            user_id=request.user.id,
            action="submit_assessment",
            entity="assessment",
            entity_id=assessment.id,
            org_id=assessment.org_id
        )

        return Response({"message": "Assessment submitted"}, status=status.HTTP_200_OK)
    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        assessment = self.get_object()

        try:
            validate_transition(
                entity="assessment",
                action="approve",
                current_status=assessment.status,
                role=request.user.role,
                context={
                    "assessment_status": assessment.status,
                    "org_id": assessment.org_id,
                    "user_org": request.user.org_id,
                }
            )
        except WorkflowForbidden as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except WorkflowConflict as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

        assessment.status = "approved"
        assessment.save(update_fields=["status"])

        log_audit_event(
            user_id=request.user.id,
            action="approve_assessment",
            entity="assessment",
            entity_id=assessment.id,
            org_id=assessment.org_id
        )

        return Response({"message": "Assessment approved"}, status=status.HTTP_200_OK)
    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        assessment = self.get_object()

        try:
            validate_transition(
                entity="assessment",
                action="reject",
                current_status=assessment.status,
                role=request.user.role,
                context={
                    "assessment_status": assessment.status,
                    "org_id": assessment.org_id,
                    "user_org": request.user.org_id,
                }
            )
        except WorkflowForbidden as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except WorkflowConflict as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

        assessment.status = "in_progress"
        assessment.save(update_fields=["status"])

        log_audit_event(
            user_id=request.user.id,
            action="reject_assessment",
            entity="assessment",
            entity_id=assessment.id,
            org_id=assessment.org_id
        )

        return Response({"message": "Assessment rejected"}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        if self.request.user.role != 'Admin':
            raise PermissionDenied("Only admins can create assessments")

        serializer.save()
