from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.workflow.engine import validate_transition
from apps.workflow.exceptions import WorkflowForbidden, WorkflowConflict

from .models import Assessment
from .serializers import AssessmentSerializer
from apps.audit.services import log_audit_event


class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Assessment.objects.filter(org_id=self.request.user.org_id)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        assessment = self.get_object()

        try:
            validate_transition(
                "assessment",
                "submit",
                assessment.status,
                request.user.role,
                {
                    "assessment_status": assessment.status,
                    "org_id": assessment.org_id,
                    "user_org": request.user.org_id,
                }
            )
        except WorkflowForbidden as e:
            return Response({"detail": str(e)}, status=403)
        except WorkflowConflict as e:
            return Response({"detail": str(e)}, status=409)

        assessment.status = "submitted"
        assessment.save()

        log_audit_event(
            request.user.id,
            "submit_assessment",
            "assessment",
            assessment.id,
            assessment.org_id
        )

        return Response({"message": "Submitted"}, status=200)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        assessment = self.get_object()

        try:
            validate_transition(
                "assessment",
                "approve",
                assessment.status,
                request.user.role,
                {
                    "assessment_status": assessment.status,
                    "org_id": assessment.org_id,
                    "user_org": request.user.org_id,
                }
            )
        except WorkflowForbidden as e:
            return Response({"detail": str(e)}, status=403)
        except WorkflowConflict as e:
            return Response({"detail": str(e)}, status=409)

        assessment.status = "approved"
        assessment.save()

        log_audit_event(
            request.user.id,
            "approve_assessment",
            "assessment",
            assessment.id,
            assessment.org_id
        )

        return Response({"message": "Approved"}, status=200)
