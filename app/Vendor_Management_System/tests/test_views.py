import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vendor_Management_System.settings')
django.setup()

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from vendor_api.models import Vendor, PurchaseOrder
from rest_framework_simplejwt.tokens import AccessToken 


# @pytest.mark.django_db
# def test_vendor_list_create_api_view():
#     user = User.objects.create_user(username='testuser', password='testpassword')
#     token = AccessToken.for_user(user)
    
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))
    
#     url = reverse('vendor-create-list')
#     data = {
#         'name': 'Test Vendor',
#         'contact_details': 'test@example.com',
#         'address': '123 Test St',
#         'vendor_code': 'TEST123'
#     }
#     response = client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_201_CREATED

def create_test_user():
    """Creates a dedicated test user with appropriate permissions."""
    username = "test_user"
    password = "strong_password"  # Replace with a strong password
    email = "test@example.com"  # Optional, can be left blank

    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, email, password)
        # Add necessary permissions to the user here (if applicable)
        # For example:
        # from your_app.models import Vendor
        # user.has_perm('your_app.add_vendor')  # Grant permission to create vendors
        print(f"Test user '{username}' created successfully.")
    else:
        print(f"Test user '{username}' already exists.")

if __name__ == "__main__":
    create_test_user()
    
@pytest.fixture(scope="function")
def jwt_token():
  """Retrieves the test user and generates a JWT token."""
  user = User.objects.get(username="test_user")
  from rest_framework_simplejwt.tokens import RefreshToken
  refresh = RefreshToken.for_user(user)
  token = refresh.access_token

  # Set the Authorization header for the client
  client = APIClient()
  client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
  return client

@pytest.fixture(scope="function")
def clean_db():
  """Fixture to ensure a clean database for each test."""
  from django.db import connections
  with connections['default'].cursor() as cursor:
    cursor.execute("DELETE FROM vendor_api_vendor")
  yield  # Test execution happens here
  # No further actions needed after the test

@pytest.mark.usefixtures("clean_db", "jwt_token")
def test_create_vendor(jwt_token):
  """Tests creating a vendor with a JWT token."""
  vendor_data = {
    "name": "Test Vendor",
    "contact_details": "123-456-7890",
    "address": "123 Main St",
    "vendor_code": "ABC123",
  }
  response = jwt_token.post("/api/vendors/", vendor_data, format="json")
  assert response.status_code == 201
  assert Vendor.objects.count() == 1
    
 