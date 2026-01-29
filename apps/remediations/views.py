from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Remediation
from .serializers import RemediationSerializer
from apps.workflow.engine import validate_transition
from apps.audit.utils import log_event


# -------------------------
# RENEWAL (Admin only)
# -------------------------
class RenewalViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "Admin":
            raise PermissionDenied("Only admins can schedule renewals")

        serializer.save()


# -------------------------
# REMEDIATION
# -------------------------
class RemediationViewSet(ModelViewSet):
    queryset = Remediation.objects.all()
    serializer_class = RemediationSerializer
    permission_classes = [IsAuthenticated]

    # -------------------------
    # CREATE → Reviewer only
    # -------------------------
    def perform_create(self, serializer):
        if self.request.user.role != "Reviewer":
            raise PermissionDenied("Only reviewers can create remediations")

        serializer.save()

    # -------------------------
    # UPDATE → Workflow controlled
    # -------------------------
    def perform_update(self, serializer):
        remediation = self.get_object()
        user = self.request.user
        new_status = self.request.data.get("status")

        # 🔒 Vendor can modify ONLY their own remediation
        if user.role == "Vendor":
            if remediation.assessment.vendor.user != user:
                raise PermissionDenied("You cannot modify this remediation")

        # 🔒 Admin is read-only
        if user.role == "Admin":
            raise PermissionDenied("Admin cannot modify remediation")

        # -------------------------
        # STATUS CHANGE
        # -------------------------
        if new_status and new_status != remediation.status:

            # 🔁 Map transition → action
            if remediation.status == "Open" and new_status == "In Progress":
                action = "start"

                if user.role != "Vendor":
                    raise PermissionDenied("Only vendor can start remediation")

            elif remediation.status == "In Progress" and new_status == "Submitted":
                action = "submit"

                if user.role != "Vendor":
                    raise PermissionDenied("Only vendor can submit remediation")

            elif remediation.status == "Submitted" and new_status == "Closed":
                action = "close"

                if user.role != "Reviewer":
                    raise PermissionDenied("Only reviewer can close remediation")

            else:
                raise ValidationError(
                    "Invalid remediation status transition",
                    code=409
                )

            try:
                # 🔑 Central workflow validation
                validate_transition(remediation, action, user.role)

                serializer.save()

                log_event(
                    user=user,
                    action=action,
                    entity="Remediation",
                    entity_id=remediation.id,
                    success=True
                )

            except Exception as e:
                log_event(
                    user=user,
                    action=action,
                    entity="Remediation",
                    entity_id=remediation.id,
                    success=False,
                    error_message=str(e)
                )
                raise

        else:
            # Non-status update (e.g., evidence upload)
            serializer.save()
