from django.apps import AppConfig

class AppClaimsConfig(AppConfig):
    """
    Configuration for the 'claims' app within the Django project.
    
    Sets the default field type for auto-created primary keys to 'BigAutoField'
    to support a larger number of objects, and specifies the app name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "claims"
