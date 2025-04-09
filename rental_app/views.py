from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from .models import Property, Tenant, Lease, Payment, Maintenance
from .serializers import PropertySerializer, TenantSerializer, LeaseSerializer, PaymentSerializer, MaintenanceSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter properties by owner (current user)
        return Property.objects.filter(owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return statistics about properties"""
        properties = self.get_queryset()
        total = properties.count()
        occupied = properties.filter(status='occupied').count()
        available = properties.filter(status='available').count()
        
        return Response({
            'total': total,
            'occupied': occupied,
            'available': available,
            'occupancy_rate': (occupied / total * 100) if total > 0 else 0
        })

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Get tenants related to properties owned by current user
        return Tenant.objects.filter(leases__property__owner=self.request.user).distinct()

class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter leases by property owner (current user)
        return Lease.objects.filter(property__owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Return leases expiring in the next 30 days"""
        today = timezone.now().date()
        thirty_days_later = today + timedelta(days=30)
        
        leases = self.get_queryset().filter(
            end_date__gte=today,
            end_date__lte=thirty_days_later,
            status='active'
        )
        
        serializer = self.get_serializer(leases, many=True)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter payments by property owner (current user)
        return Payment.objects.filter(lease__property__owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Return overdue payments"""
        today = timezone.now().date()
        
        payments = self.get_queryset().filter(
            due_date__lt=today,
            status='pending'
        )
        
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Return payments due in the next 30 days"""
        today = timezone.now().date()
        thirty_days_later = today + timedelta(days=30)
        
        payments = self.get_queryset().filter(
            due_date__gte=today,
            due_date__lte=thirty_days_later,
            status='pending'
        )
        
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def monthly_income(self, request):
        """Return monthly income for the current year"""
        current_year = timezone.now().year
        
        monthly_data = []
        for month in range(1, 13):
            payments = self.get_queryset().filter(
                payment_date__year=current_year,
                payment_date__month=month,
                status='paid'
            )
            
            total = payments.aggregate(total=Sum('amount'))['total'] or 0
            
            monthly_data.append({
                'month': month,
                'total': total
            })
        
        return Response(monthly_data)

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter maintenance requests by property owner (current user)
        return Maintenance.objects.filter(property__owner=self.request.user)


