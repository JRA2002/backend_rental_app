from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, TenantViewSet, LeaseViewSet, PaymentViewSet, MaintenanceViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'tenants', TenantViewSet)
router.register(r'leases', LeaseViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'maintenance', MaintenanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


