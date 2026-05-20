from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from system_management.models import CustomUser
from ms_identity_web.django.middleware import MsalMiddleware
from django.http import HttpResponse
class ClaimsViewTests(TestCase):

    @patch('googlemaps.Client.distance_matrix')
    #@patch('ms_identity_web.django.middleware.MsalMiddleware.__call__')  # Adjust the patching target based on your setup
    def test_claims_view_post_success(self, mock_distance_matrix):
        # Mock Google Maps distance matrix response
        mock_distance_matrix.return_value = {
            'status': 'OK',
            'rows': [
                {
                    'elements': [
                        {'distance': {'value': 10000}}  # 10 km distance
                    ]
                }
            ]
        }
    

        # Mock the middleware to pass through
        # mock_msal_middleware.return_value = HttpResponse("Mocked Response")
        
        # Create a user and log them in
        user = CustomUser.objects.create_user(email="testuser@example.com", password="testpass")
        login_successful = self.client.login(email=user.email, password="testpass")
        self.assertTrue(login_successful)

        # Prepare POST data
        post_data = {
            'consultant_address': '123 Test St',
            'client_address': '456 Client Rd',
            'trip_count': 1,
            'description': 'Test trip'
        }

        # Send POST request to the claims view
        response = self.client.post(reverse('get_claims_by_user'), data=post_data)
        print("The response in test is:",response)

        #self.assertIsInstance(response, MagicMock)  # Check if response is the correct type
    
        # # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # # # Ensure the correct template is used
        # self.assertTemplateUsed(response, 'claims/claims.html')

        # # # Check that the success message is in the response content
        # self.assertContains(response, 'Submitted successfully')
        # Ensure the response is an HTTP response
        self.assertIsInstance(response, HttpResponse)

        # Check that a template is used in the response
        #self.assertIn('claims/claims.html', [ response.templates])
        #print("The templates are:",response.templates)
        # Check that the success message is in the response content
        #self.assertContains(response, 'Submitted successfully')