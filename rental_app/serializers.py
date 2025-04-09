from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Property, Tenant, Lease, Payment, Maintenance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class PropertySerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = '__all__'
    
    def get_owner_name(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}"

class TenantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Tenant
        fields = '__all__'

class LeaseSerializer(serializers.ModelSerializer):
    property_title = serializers.SerializerMethodField()
    tenant_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Lease
        fields = '__all__'
    
    def get_property_title(self, obj):
        return obj.property.title
    
    def get_tenant_name(self, obj):
        return f"{obj.tenant.user.first_name} {obj.tenant.user.last_name}"

class PaymentSerializer(serializers.ModelSerializer):
    property_title = serializers.SerializerMethodField()
    tenant_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = '__all__'
    
    def get_property_title(self, obj):
        return obj.lease.property.title
    
    def get_tenant_name(self, obj):
        return f"{obj.lease.tenant.user.first_name} {obj.lease.tenant.user.last_name}"

class MaintenanceSerializer(serializers.ModelSerializer):
    property_title = serializers.SerializerMethodField()
    tenant_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Maintenance
        fields = '__all__'
    
    def get_property_title(self, obj):
        return obj.property.title
    
    def get_tenant_name(self, obj):
        return f"{obj.tenant.user.first_name} {obj.tenant.user.last_name}"

