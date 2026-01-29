from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response

from .models import Renewal
from .serializers import RenewalSerializer

from apps.workflow.engine import validate_transition
from apps.workflow.exceptions import WorkflowForbidden, WorkflowConflict
from apps.audit.services import log_audit_event


class RenewalViewSet(ModelViewSet):
    serializer_class = RenewalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 🔒 Tenant isolation
        return Renewal.objects.filter(org_id=self.request.user.org_id)

    # -------------------------
    # UPDATE RENEWAL
    # Admin only, workflow controlled
    # -------------------------
    def update(self, request, *args, **kwargs):
        renewal = self.get_object()
        user = request.user
        from_status = renewal.status
        to_status = request.data.get("status")

        # 🔒 Role enforcement
        if user.role != "Admin":
            raise PermissionDenied("Only Admin can update renewal status")

        if to_status and to_status != from_status:

            # Map status change → workflow action
            transition_map = {
                ("pending", "approved"): "approve",
                ("pending", "rejected"): "reject",
            }

            action = transition_map.get((from_status, to_status))
            if not action:
                raise WorkflowConflict("Invalid renewal status transition")

            try:
                validate_transition(
                    entity="renewal",
                    action=action,
                    current_status=from_status,
                    role=user.role,
                    context={
                        "previous_assessment_closed": True,  # verified externally
                        "org_id": renewal.org_id,
                        "user_org": user.org_id,
                    }
                )
            except WorkflowForbidden as e:
                return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
            except WorkflowConflict as e:
                return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

            renewal.status = to_status
            renewal.save(update_fields=["status"])

            log_audit_event(
                user_id=user.id,
                action=f"RENEWAL_{action.upper()}",
                entity="renewal",
                entity_id=renewal.id,
                from_status=from_status,
                to_status=to_status,
                org_id=renewal.org_id
            )

            return Response(
                {"message": f"Renewal {to_status}"},
                status=status.HTTP_200_OK
            )

        # Non-status update
        return super().update(request, *args, **kwargs)
