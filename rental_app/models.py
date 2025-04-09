from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    PROPERTY_STATUS = (
        ('available', 'Disponible'),
        ('occupied', 'Ocupado'),
    )
    
    PROPERTY_TYPE = (
        ('apartment', 'Apartamento'),
        ('house', 'Casa'),
        ('studio', 'Estudio'),
        ('commercial', 'Comercial'),
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=100)
    address = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE)
    status = models.CharField(max_length=20, choices=PROPERTY_STATUS, default='available')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveSmallIntegerField(default=1)
    bathrooms = models.PositiveSmallIntegerField(default=1)
    area = models.PositiveIntegerField(help_text="Área en metros cuadrados")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"

class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile')
    phone = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "Inquilino"
        verbose_name_plural = "Inquilinos"

class Lease(models.Model):
    LEASE_STATUS = (
        ('active', 'Activo'),
        ('expired', 'Expirado'),
        ('terminated', 'Terminado'),
    )
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='leases')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='leases')
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=LEASE_STATUS, default='active')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.property.title} - {self.tenant}"
    
    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('late', 'Atrasado'),
        ('cancelled', 'Cancelado'),
    )
    
    PAYMENT_METHOD = (
        ('cash', 'Efectivo'),
        ('bank_transfer', 'Transferencia Bancaria'),
        ('credit_card', 'Tarjeta de Crédito'),
        ('check', 'Cheque'),
    )
    
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Pago {self.id} - {self.lease}"
    
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

class Maintenance(models.Model):
    REQUEST_STATUS = (
        ('pending', 'Pendiente'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    )
    
    REQUEST_PRIORITY = (
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('emergency', 'Emergencia'),
    )
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_requests')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='maintenance_requests')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='pending')
    priority = models.CharField(max_length=20, choices=REQUEST_PRIORITY, default='medium')
    request_date = models.DateField(auto_now_add=True)
    scheduled_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.property.title}"
    
    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"

