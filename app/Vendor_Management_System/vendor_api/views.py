from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Vendor
from .serializers import VendorSerializer

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