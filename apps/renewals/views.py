from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Renewal
from .serializers import RenewalSerializer
from apps.workflow.engine import validate_transition
from apps.audit.utils import log_event

class RenewalViewSet(ModelViewSet):
    queryset = Renewal.objects.all()
    serializer_class = RenewalSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        renewal = self.get_object()
        new_status = self.request.data.get("status")

        if new_status and new_status != renewal.status:
            try:
                validate_transition(
                    renewal,
                    "renew",
                    self.request.user.role
                )
                serializer.save()
                log_event(
                    self.request.user,
                    "renew",
                    "Renewal",
                    renewal.id,
                    True
                )
            except Exception as e:
                log_event(
                    self.request.user,
                    "renew",
                    "Renewal",
                    renewal.id,
                    False,
                    str(e)
                )
                raise
        else:
            serializer.save()
