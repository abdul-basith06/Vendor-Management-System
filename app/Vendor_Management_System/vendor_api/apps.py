from django.apps import AppConfig


class VendorApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vendor_api"
    
    def ready(self):
        from . import signals
