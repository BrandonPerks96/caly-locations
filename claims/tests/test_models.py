from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from ..models import Claim  # Relative import

class ClaimModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="password123"
        )

        self.claim = Claim.objects.create(
            consultant_address="123 Consultant St",
            client_address="456 Client Ave",
            total_distance=Decimal("120.50"),
            trip_count=3,
            amount=Decimal("250.00"),
            description="Business trip to client site",
            user=self.user
        )

    def test_claim_fields(self):
        claim = self.claim
        self.assertEqual(claim.consultant_address, "123 Consultant St")
        self.assertEqual(claim.client_address, "456 Client Ave")
        self.assertEqual(claim.total_distance, Decimal("120.50"))
        self.assertEqual(claim.trip_count, 3)
        self.assertEqual(claim.amount, Decimal("250.00"))
        self.assertEqual(claim.description, "Business trip to client site")
        self.assertEqual(claim.user, self.user)

    def test_claim_str(self):
        claim = self.claim
        self.assertEqual(str(claim), self.user.email)

    def test_auto_populated_fields(self):
        claim = self.claim
        self.assertIsNotNone(claim.created)
