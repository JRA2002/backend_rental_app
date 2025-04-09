from django.contrib import admin
from .models import Property, Tenant, Lease, Payment, Maintenance

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'property_type', 'status', 'price')
    list_filter = ('status', 'property_type')
    search_fields = ('title', 'address')

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone')
    search_fields = ('user__first_name', 'user__last_name', 'phone')

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'start_date', 'end_date', 'rent_amount', 'status')
    list_filter = ('status',)
    search_fields = ('property__title', 'tenant__user__first_name', 'tenant__user__last_name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('lease', 'amount', 'due_date', 'payment_date', 'status')
    list_filter = ('status', 'payment_method')
    search_fields = ('lease__property__title', 'lease__tenant__user__first_name', 'lease__tenant__user__last_name')

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'property', 'tenant', 'status', 'priority', 'request_date')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'property__title', 'tenant__user__first_name', 'tenant__user__last_name')


