from rest_framework.routers import DefaultRouter
from .views import RemediationViewSet

router = DefaultRouter()
router.register("remediations", RemediationViewSet)

urlpatterns = router.urls
