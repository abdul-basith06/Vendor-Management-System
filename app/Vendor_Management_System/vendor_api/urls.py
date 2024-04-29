from django.urls import path
from .views import VendorListCreateAPIView, VendorRetrieveUpdateDestroyView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="get-token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-create-list'),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-read-update-delete'),
]
