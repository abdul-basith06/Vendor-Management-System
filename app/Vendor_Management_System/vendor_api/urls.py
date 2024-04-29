from django.urls import path
from .views import (
    VendorListCreateAPIView,
    VendorRetrieveUpdateDestroyView,
    PurchaseOrderListCreateAPIView,
    PurchaseOrderRetrieveUpdateDestroyView,
    PurchaseOrderAcknowledgeView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="get-token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-create-list'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-read-update-delete'),
    path('purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-create-list'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDestroyView.as_view(), name='purchase-order-read-update-delete'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', PurchaseOrderAcknowledgeView.as_view(), name='purchase-order-acknowledge'),
]
