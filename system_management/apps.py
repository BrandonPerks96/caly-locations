from django.apps import AppConfig

class SystemManagementConfig(AppConfig):
    """
    Django application configuration for the System Management app.
    
    This configuration helps with defining certain app-wide properties like
    the default field types for database columns and the app's internal name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "system_management"
