from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.not_found import NotFound # type: ignore
from django.db.models import Q

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
        return self.get_queryset().get(pk=pk)    
    
    
class PurchaseOrderListCreateAPIView(ListCreateAPIView):
    """
    API endpoint to list and create purchase orders with vendor filtering.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [OrderingFilter]  

    def get(self, request):
        """
        Retrieve a list of purchase orders.
        """
        queryset = self.get_queryset()
        vendor_id = request.query_params.get('vendor')
        if vendor_id:
            queryset = queryset.filter(Q(vendor__id=vendor_id))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            raise NotFound('Purchase order with ID ' + str(pk) + ' not found.')    
    