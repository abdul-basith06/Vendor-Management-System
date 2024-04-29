from datetime import timezone
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django.http import Http404
from django.db.models import Q, F, Avg

from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorListCreateAPIView(ListCreateAPIView):
    """
    API endpoint for creating and listing vendors.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    

class VendorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific vendor.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Override to filter by vendor ID from the URL segment.
        """
        pk = self.kwargs['vendor_id']
        try:
            return self.get_queryset().get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404('Vendor with ID ' + str(pk) + ' not found.')   
    
    
class PurchaseOrderListCreateAPIView(ListCreateAPIView):
    """
    API endpoint to list and create purchase orders with vendor filtering.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [OrderingFilter]  

    def get_queryset(self):
        """
        Override to filter by vendor (optional parameter in query string).
        """
        queryset = self.queryset
        vendor_id = self.request.query_params.get('vendor')
        if vendor_id:
            queryset = queryset.filter(Q(vendor__id=vendor_id))
        return queryset

    def post(self, request):
        """
        Create a purchase order.
        """
        serializer = PurchaseOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class PurchaseOrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, and delete a specific purchase order.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_object(self):
        """
        Override to handle 404 (Not Found) for missing purchase orders.
        """
        pk = self.kwargs.get('po_id')
        try:
            return self.queryset.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Http404('Purchase order with ID ' + str(pk) + ' not found.')    
        
        
class PurchaseOrderAcknowledgeView(UpdateAPIView):
    """
    API endpoint to acknowledge a PO by the vendor.
    """
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

    def perform_update(self, serializer):
        """
        Acknowledge a purchase order and update vendor's average response time.
        """
        serializer.save(acknowledgment_date=timezone.now())
        
        # Calculate new delivery date (Estimated date - 5 days after vendor acknowledgement)
        acknowledgment_date = serializer.instance.acknowledgment_date
        new_delivery_date = acknowledgment_date + timezone.timedelta(days=5)
        serializer.instance.delivery_date = new_delivery_date
        serializer.instance.save()
        
        # Update average response time for the vendor 
        purchase_order = serializer.instance
        vendor = purchase_order.vendor
        if vendor:
            avg_response_time = PurchaseOrder.objects.filter(
                vendor=vendor, acknowledgment_date__isnull=False
            ).aggregate(
                avg_response_time=Avg(F('acknowledgment_date') - F('issue_date'))
            )['avg_response_time']
            
            avg_response_time = round(avg_response_time, 2)

            vendor.average_response_time = avg_response_time
            vendor.save()
        
    