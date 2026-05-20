from django.urls import path
from . import views

# Define URL patterns for the application, specifying the endpoint for the home page and its redirect.
urlpatterns = [
    path('', views.index_redirect, name='index_redirect'),  # Redirects requests to the root URL
    path('index/', views.index, name='index'),  # Serves the main index page
    path('auth/', views.auth_redirect, name='auth'),  # Authorizes the user and redirects to the claims page
    path('pdf/', views.download_pdf, name='download_pdf'),  # Downloads the PDF file
]

