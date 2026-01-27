from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Remediation
from .serializers import RemediationSerializer
from apps.workflow.engine import validate_transition
from apps.audit.utils import log_event

class RemediationViewSet(ModelViewSet):
    queryset = Remediation.objects.all()
    serializer_class = RemediationSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        remediation = self.get_object()
        new_status = self.request.data.get("status")

        if new_status and new_status != remediation.status:
            try:
                validate_transition(
                    remediation,
                    "close",
                    self.request.user.role
                )
                serializer.save()
                log_event(
                    self.request.user,
                    "close",
                    "Remediation",
                    remediation.id,
                    True
                )
            except Exception as e:
                log_event(
                    self.request.user,
                    "close",
                    "Remediation",
                    remediation.id,
                    False,
                    str(e)
                )
                raise
        else:
            serializer.save()
