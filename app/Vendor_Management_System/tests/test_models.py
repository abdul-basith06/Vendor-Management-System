# import os
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vendor_Management_System.settings')
# django.setup()

# from django.test import TestCase
# from django.db import IntegrityError

# from vendor_api.models import Vendor

# class TestVendorModel(TestCase):

#     def test_create_vendor(self):
#         """
#         Test creating a new vendor object with valid data.
#         """
#         vendor = Vendor.objects.create(
#             name="Test Vendor",
#             contact_details="test@example.com",
#             address="123 Main St",
#             vendor_code="ABC123"
#         )
#         self.assertEqual(vendor.name, "Test Vendor")
#         self.assertEqual(vendor.contact_details, "test@example.com")
#         self.assertEqual(vendor.address, "123 Main St")
#         self.assertEqual(vendor.vendor_code, "ABC123")

#     def test_unique_vendor_code(self):
#         """
#         Test that vendor code must be unique.
#         """
#         Vendor.objects.create(
#             name="Vendor 1",
#             contact_details="test1@example.com",
#             address="1 Main St",
#             vendor_code="UNIQUE_CODE"
#         )
#         with self.assertRaises(IntegrityError):
#             Vendor.objects.create(
#                 name="Vendor 2",
#                 contact_details="test2@example.com",
#                 address="2 Main St",
#                 vendor_code="UNIQUE_CODE"
#             )  # Duplicate vendor code

#     def test_vendor_str_representation(self):
#         """
#         Test the string representation of the Vendor model.
#         """
#         vendor = Vendor.objects.create(
#             name="Test Vendor",
#             contact_details="test@example.com",
#             address="123 Main St",
#             vendor_code="ABC123"
#         )
#         self.assertEqual(str(vendor), vendor.name)

#     def test_vendor_on_time_delivery_rate_calculation_no_orders(self):
#         """
#         Test on-time delivery rate calculation when there are no orders.
#         """
#         vendor = Vendor.objects.create(
#             name="Test Vendor",
#             contact_details="test@example.com",
#             address="123 Main St",
#             vendor_code="ABC123"
#         )
#         self.assertIsNone(vendor.calculate_on_time_delivery_rate())

#     # def test_vendor_on_time_delivery_rate_calculation_with_orders(self):
#     #     """
#     #     Test on-time delivery rate calculation with completed and pending orders.
#     #     """
#     #     vendor = Vendor.objects.create(
#     #         name="Test Vendor",
#     #         contact_details="test@example.com",
#     #         address="123 Main St",
#     #         vendor_code="ABC123"
#     #     )
#     #     # Create completed purchase orders for the vendor
#     #     completed_orders = [
#     #         vendor.purchaseorder_set.create(status='completed', delivery_date='2024-05-01') for _ in range(5)
#     #     ]
#     #     # Create pending purchase orders for the vendor
#     #     pending_orders = [
#     #         vendor.purchaseorder_set.create(status='pending') for _ in range(3)
#     #     ]
#     #     expected_delivery_rate = (len(completed_orders) / (len(completed_orders) + len(pending_orders))) * 100
#     #     self.assertAlmostEqual(vendor.calculate_on_time_delivery_rate(), expected_delivery_rate, places=2)
