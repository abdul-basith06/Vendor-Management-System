from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vendor model.
    """
    class Meta:
        model = Vendor
        fields = '__all__'  

class PurchaseOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the PurchaseOrder model.
    """
    class Meta:
        model = PurchaseOrder
        fields = '__all__'  

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the HistoricalPerformance model (optional).
    """
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'  
