import logging
import os
import googlemaps
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.views.generic import View
from django.conf import settings
from app.settings.nonprod import GOOGLE_API_KEY, MS_IDENTITY_WEB, CSRF_TRUSTED_ORIGINS
import requests
from .models import Claim
from django.db import IntegrityError
from django.contrib import messages
from system_management.models import CustomUser
import json
 

ms_identity_web = MS_IDENTITY_WEB

hostname = CSRF_TRUSTED_ORIGINS

google_maps_api_key = GOOGLE_API_KEY 


gmaps = googlemaps.Client(key=google_maps_api_key)

logger = logging.getLogger(__name__)

# Create your views here.

@ms_identity_web.login_required
def maps_api_proxy(request):
    """
    A view function that acts as a proxy for the Google Maps API.
    
    This function requires the user to be authenticated with the Microsoft Identity Web library.
    
    Parameters:
        - request (HttpRequest): The HTTP request object.
        
    Returns:
        - HttpResponse: The response from the Google Maps API, with the content type set to 'application/javascript'.
        
    Raises:
        - HttpResponseBadRequest: If the API key is not found.
        - HttpResponse: If the request to the Google Maps API fails.
    """
    api_key = settings.GOOGLE_API_KEY
    params = request.GET.dict()
    
    if not api_key:
        logger.error("API key not found.")
        return HttpResponseBadRequest("API key not found.")
    
    params['key'] = api_key
    if 'libraries' not in params:
        params['libraries'] = 'places'
    if 'callback' not in params:
        params['callback'] = 'initMap'
    
    url = 'https://maps.googleapis.com/maps/api/js'
    
    logger.debug(f'Sending request to Google Maps API with params: {params}')
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        logger.error(f'Failed to fetch the Maps API: {response.status_code}')
        return HttpResponse(f'Failed to fetch the Maps API: {response.status_code}', status=response.status_code)
    
    logger.debug(f'Google Maps API response (truncated): {response.text[:500]}')
    
    return HttpResponse(response.text, content_type='application/javascript')
    

@ms_identity_web.login_required
def claims(request):
    """
    A view function that handles user claims. It processes the POST request data to calculate the amount based 
    on the distance between the consultant and client addresses. It then creates a new claim object and saves it 
    to the database. Returns a success message upon successful submission and an error message if the data saving fails.
    """

    user_email_str = request.identity_context_data._token_cache
    user_email_dict = json.loads(user_email_str)
    user_email = None

    for key, value in user_email_dict.get("Account", {}).items():
        if "username" in value:
            user_email = value["username"]
            break
    else:
        return HttpResponseBadRequest("Error getting user email")

    # Calculate the total amount of the claim based on the distance
    km_0_50 = 4.95
    km_51_100 = 3.71
    km_101_150 = 2.48
    amount = 0

    context = {
        # Google Maps API key for the frontend to use
        'google_maps_api_key': google_maps_api_key,
        # The username to display in the template
        'active_user': user_email,
        'hostname' : hostname,
        # SARS rates
        "rate_0_50": km_0_50,
        "rate_51_100": km_51_100,
        "rate_101_160": km_101_150
    }

    if request.method == 'POST':
        user = CustomUser.objects.get(email=user_email)
        consultant_address = request.POST.get('consultant_address', '')
        client_address = request.POST.get('client_address', '')
        trip_count = int(request.POST.get('trip_count'))
        description = request.POST.get('description', '')

        # Get the distance between the consultant and client addresses
        distance_result = gmaps.distance_matrix(consultant_address, client_address, mode='driving')

        if distance_result['status'] == 'OK':
            total_distance = (distance_result['rows'][0]['elements'][0]['distance']['value'] / 1000) * 2
        else:
            return HttpResponseBadRequest("Error getting distance: " + distance_result['status'])

        if total_distance > 160:
            amount += ((60 * km_101_150) + (50 * km_51_100) + (50 * km_0_50)) * trip_count
        elif total_distance > 100:
            distance_100 = total_distance - 100
            amount += ((distance_100 * km_101_150) + (50 * km_51_100) + (50 * km_0_50)) * trip_count
        elif total_distance > 50:
            distance_50 = total_distance - 50
            amount += ((distance_50 * km_51_100) + (50 * km_0_50)) * trip_count
        else:
            amount += (total_distance * km_0_50) * trip_count

        # Create a new claim object and save it to the database
        new_claim = Claim(consultant_address=consultant_address,
                          client_address=client_address,
                          total_distance=total_distance,
                          trip_count=trip_count,
                          amount=amount,
                          description=description,
                          user=user)
        try:
            new_claim.save()
            return HttpResponse("Submitted successfully")
        except IntegrityError as e:
            return HttpResponseBadRequest("Error saving data: " + str(e))

    return render(request, 'claims/claims.html', context)


@ms_identity_web.login_required
def get_claims_by_user(request):
    """
    Retrieves all claims associated with the current user.

    Parameters:
        - request (HttpRequest): The HTTP request object.

    Returns:
        - JsonResponse: A JSON response containing the list of claims associated with the user.
    """

    if request.method == 'GET':
        user_email_str = request.identity_context_data._token_cache
        user_email_dict = json.loads(user_email_str)
        user_email = None
        
        for key, value in user_email_dict.get("Account", {}).items():
            if "username" in value:
                user_email = value["username"]
                break
        else:
            return HttpResponseBadRequest("Error getting user email")

        user = CustomUser.objects.get(email=user_email)
        claims = Claim.objects.filter(user_id=user.id)
        data = list(claims.values())
        return JsonResponse({'data': data})

    return HttpResponseNotFound()



@ms_identity_web.login_required
def view_claims_by_id(request, id):
    """
    Retrieves a claim by its ID and renders the claim view page.

    Parameters:
        - request (HttpRequest): The HTTP request object.
        - id (int): The ID of the claim to be viewed.

    Returns:
        - HttpResponse: The rendered claim view page if the claim exists and the user is authenticated.
        - HttpResponseNotFound: If the claim does not exist.
        - HttpResponseBadRequest: If there is an error getting the user email.
    """

    user_email_str = request.identity_context_data._token_cache
    user_email_dict = json.loads(user_email_str)
    user_email = None

    for key, value in user_email_dict.get("Account", {}).items():
        if "username" in value:
            user_email = value["username"]
            break
    else:
        return HttpResponseBadRequest("Error getting user email")

    if request.method == 'GET':
        try:
            claim = Claim.objects.get(id=id)
            user = CustomUser.objects.get(email=user_email)

            # Check if the claim belongs to the authenticated user
            if claim.user_id != user.id:
                return HttpResponseForbidden("You are not authorized to view this claim.")
            
            name = claim.user.get_full_name()
            context = {
                'claim': claim,
                'google_maps_api_key': google_maps_api_key,
                'username': name,
                'active_user': user_email,
            }
            return render(request, 'claims/claims_view.html', context)
        except Claim.DoesNotExist:
            return HttpResponseNotFound('Claim not found')


from decimal import Decimal

@ms_identity_web.login_required
def claims_preview(request, id):

    # Calculate the total amount of the claim based on the distance
    km_0_50 = Decimal('4.86')
    km_51_100 = Decimal('3.65')
    km_101_160 = Decimal('2.43')
    amount = Decimal('0')
    distance_50 = Decimal('0')
    distance_100 = Decimal('0')

    # Get the user email from the token cache
    user_email_str = request.identity_context_data._token_cache
    user_email_dict = json.loads(user_email_str)
    user_email = None

    for key, value in user_email_dict.get("Account", {}).items():
        if "username" in value:
            user_email = value["username"]
            break
    else:
        return HttpResponseBadRequest("Error getting user email")
    
    # Get specific claim data
    if request.method == 'GET':

        claim = Claim.objects.get(id=id)
        user = CustomUser.objects.get(email=user_email)

        name = claim.user.get_full_name()
        claim_id = claim.id
        claim_date = claim.created
        consultant_address = claim.consultant_address
        client_address = claim.client_address
        total_distance = Decimal(claim.total_distance)
        trip_count = claim.trip_count
        tot_amount = round(claim.amount,2)
        single_amount = round(tot_amount / trip_count, 2)

        
        distance_100 = total_distance - 100 
        distance_50 = total_distance - 50


        max_50 = 50 * km_0_50
        max_100 = 50 * km_51_100
        max_160 = 60 * km_101_160
        to_50 = round(distance_50 * km_51_100, 2)
        to_100 = round(distance_100 * km_101_160, 2)

        if claim.user_id != user.id:
            return HttpResponseForbidden("You are not authorized to view this claim.")

        context = {
            'claim_id': claim_id,
            'claim_date': claim_date,
            'consultant_address': consultant_address,
            'client_address': client_address,
            'total_distance': total_distance,
            'trip_count': trip_count,
            'amount': single_amount,
            'tot_amount': tot_amount,
            'username': name,
            'active_user': user_email,
            'description': claim.description,
            'to_50': to_50,
            'to_100': to_100,
            'max_50': max_50,
            'max_100': max_100,
            'max_160': max_160,
        }


    return render(request, 'claims/claims_preview.html', context)

@ms_identity_web.login_required
def delete_claim(request, id):
    """
    Deletes a claim by its ID.

    Parameters:
        - request (HttpRequest): The HTTP request object.
        - id (int): The ID of the claim to be deleted.

    Returns:
        - HttpResponse: A success message if the claim is deleted successfully.
        - HttpResponseNotFound: If the claim does not exist.
    """

    if request.method == 'POST':
        claim_id = request.POST.get('claim_id')
        try:
            claim = Claim.objects.get(id=id)
            claim.delete()
            return JsonResponse({'status': 'success', 'message': 'Claim deleted successfully'})
        except Claim.DoesNotExist:
            return HttpResponseNotFound('Claim not found')


def logout(request):
    """
    Logout the user by clearing the session and redirecting to the Azure AD logout endpoint.
    Replace the 'tenant_id' in the URL with the tenant authority.
    
    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - Redirects the user to the Azure AD logout URL.
    """

    # Clear the user's session
    request.session.clear()

    # Redirect to Azure AD logout endpoint
    # Replace 'https://login.microsoftonline.com/{tenant_id}/oauth2/logout' with your Azure AD logout URL
    tenant = os.environ.get('AUTHORITY_LOGOUT')
    hostname = 'https://'+ os.environ.get("WEBSITE_HOSTNAME")
    

    logout_url = f'https://login.microsoftonline.com/{tenant}/oauth2/logout?post_logout_redirect_uri={hostname}'
    return redirect(logout_url)



