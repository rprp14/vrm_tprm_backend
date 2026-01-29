from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response

from .models import Remediation
from .serializers import RemediationSerializer

from apps.workflow.engine import validate_transition
from apps.workflow.exceptions import WorkflowForbidden, WorkflowConflict
from apps.audit.services import log_audit_event


# -------------------------
# REMEDIATION WORKFLOW
# -------------------------
class RemediationViewSet(ModelViewSet):
    serializer_class = RemediationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 🔒 Tenant isolation
        return Remediation.objects.filter(
            assessment__org_id=self.request.user.org_id
        )

    # -------------------------
    # CREATE REMEDIATION
    # Reviewer only
    # -------------------------
    def perform_create(self, serializer):
        if self.request.user.role != "Reviewer":
            raise PermissionDenied("Only reviewers can create remediations")

        remediation = serializer.save()

        log_audit_event(
            user_id=self.request.user.id,
            action="REMEDIATION_CREATED",
            entity="remediation",
            entity_id=remediation.id,
            from_status=None,
            to_status=remediation.status,
            org_id=remediation.assessment.org_id
        )

    # -------------------------
    # UPDATE REMEDIATION
    # Workflow controlled
    # -------------------------
    def update(self, request, *args, **kwargs):
        remediation = self.get_object()
        user = request.user
        from_status = remediation.status
        to_status = request.data.get("status")

        # 🔒 Admin is read-only
        if user.role == "Admin":
            raise PermissionDenied("Admin cannot modify remediation")

        # 🔒 Vendor can act only on own org
        if user.role == "Vendor":
            if remediation.assessment.org_id != user.org_id:
                raise PermissionDenied("Cross-tenant access blocked")

        # -------------------------
        # STATUS TRANSITION
        # -------------------------
        if to_status and to_status != from_status:

            # Map transition → workflow action
            transition_map = {
                ("open", "in_progress"): "start",
                ("in_progress", "submitted"): "submit",
                ("submitted", "closed"): "close",
                ("submitted", "reopened"): "reopen",
            }

            action = transition_map.get((from_status, to_status))
            if not action:
                raise WorkflowConflict("Invalid remediation status transition")

            try:
                validate_transition(
                    entity="remediation",
                    action=action,
                    current_status=from_status,
                    role=user.role,
                    context={
                        "evidence_uploaded": remediation.evidence.exists(),
                        "org_id": remediation.assessment.org_id,
                        "user_org": user.org_id
                    }
                )
            except WorkflowForbidden as e:
                return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
            except WorkflowConflict as e:
                return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

            remediation.status = to_status
            remediation.save(update_fields=["status"])

            log_audit_event(
                user_id=user.id,
                action=f"REMEDIATION_{action.upper()}",
                entity="remediation",
                entity_id=remediation.id,
                from_status=from_status,
                to_status=to_status,
                org_id=remediation.assessment.org_id
            )

            return Response(
                {"message": f"Remediation {to_status}"},
                status=status.HTTP_200_OK
            )

        # -------------------------
        # NON-STATUS UPDATE
        # (e.g. evidence upload)
        # -------------------------
        return super().update(request, *args, **kwargs)
