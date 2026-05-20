from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

class Claim(models.Model):
    """
    Model representing a claim with details of trips made by consultants.

    Attributes:
        consultant_address (str): Address of the consultant.
        client_address (str): Address of the client.
        total_distance (Decimal): Total distance traveled for the claim.
        trip_count (int): Number of trips made.
        amount (Decimal): Amount claimed.
        description (str): Description of the claim.
        created (DateTime): The date and time when the claim was created.
        modified (DateTime): The date and time when the claim was last modified.
        user (ForeignKey): Reference to the associated user.
    """
    consultant_address = models.CharField(max_length=150)
    client_address = models.CharField(max_length=150)
    total_distance = models.DecimalField(max_digits=10, decimal_places=2)
    trip_count = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=150)

    created = models.DateTimeField(editable=False, default=now)
    modified = models.DateTimeField(default=now)

    user = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT)
 
    def __str__(self):
        return self.user.email
 
    class Meta:
        verbose_name_plural = 'Claims'
