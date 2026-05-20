from django.urls import path
from . import views

# URL patterns for claims-related actions
urlpatterns = [
    path('claims/', views.claims, name='claims'),  # Endpoint for viewing claims
    path('get_claims/', views.get_claims_by_user, name='get_claims_by_user'),  # Endpoint for retrieving claims data
    path('view_claim/<int:id>/', views.view_claims_by_id, name='view_claims_by_id'),  # Endpoint for viewing a single claim
    path('claims_preview/<int:id>/', views.claims_preview, name='claims_preview'),  # Endpoint for previewing claims
    path('delete_claim/<int:id>/', views.delete_claim, name='delete_claim'),  # Endpoint for deleting a claim
    path('maps-api-proxy/', views.maps_api_proxy, name='maps_api_proxy'),  # Endpoint for proxying the Google Maps API
    path('logout/', views.logout, name='logout')  # Endpoint for user logout
   ]