from django.urls import path
from .views import VendorListCreateAPIView, VendorRetrieveUpdateDestroyView


urlpatterns = [
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-create-list'),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-read-update-delete'),
]
