from django.contrib import admin
from .models import Claim

# Admin interface for Claim model
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    """ 
    Admin view for Claim model to customize how claims are displayed in the Django admin interface.
    """
    # Fields to display in the claim list view
    list_display = (
        'consultant_address', 
        'client_address', 
        'total_distance', 
        'trip_count', 
        'amount', 
        'description',
        'created',
        'modified',
        'user'
    )
