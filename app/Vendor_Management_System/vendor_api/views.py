from django.utils import timezone
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django.http import Http404
from django.db.models import Q, F, Avg

from .models import Vendor, PurchaseOrder
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
)


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
        pk = self.kwargs["pk"]
        try:
            return self.get_queryset().get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404("Vendor with ID " + str(pk) + " not found.")


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
        queryset = PurchaseOrder.objects.all()
        vendor_id = self.request.query_params.get("vendor")
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
        pk = self.kwargs.get("po_id")
        try:
            return self.queryset.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Http404("Purchase order with ID " + str(pk) + " not found.")


class PurchaseOrderAcknowledgeView(UpdateAPIView):
    """
    API endpoint to acknowledge a PO by the vendor.
    """

    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = "po_id"

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
                avg_response_time=Avg(F("acknowledgment_date") - F("issue_date"))
            )[
                "avg_response_time"
            ]

            average_days = avg_response_time.total_seconds() / (60 * 60 * 24)
            avg_response_time = round(average_days, 2)

            vendor.average_response_time = avg_response_time
            vendor.save()


class VendorPerformanceRetrieveView(RetrieveAPIView):
    """
    API endpoint to retrieve a vendor's performance metrics.
    """

    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = "vendor_id"

    def retrieve(self, request, *args, **kwargs):
        vendor = self.get_object()
        serializer = VendorSerializer(vendor)

        serializer.data["on_time_delivery_rate"] = vendor.on_time_delivery_rate
        serializer.data["quality_rating_avg"] = vendor.quality_rating_avg
        serializer.data["average_response_time"] = vendor.average_response_time
        serializer.data["fulfillment_rate"] = vendor.fulfillment_rate

        return Response(serializer.data)
