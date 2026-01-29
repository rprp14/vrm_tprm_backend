"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.assessments.views import AssessmentViewSet
from apps.remediations.views import RemediationViewSet
from apps.renewals.views import RenewalViewSet

# DRF router
router = DefaultRouter()
router.register("assessments", AssessmentViewSet, basename="assessment")
router.register("remediations", RemediationViewSet, basename="remediation")
router.register("renewals", RenewalViewSet, basename="renewal")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include("apps.accounts.urls")),
    
]

