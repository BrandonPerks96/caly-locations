from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.http import FileResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import json
import os

# Initialize settings for Microsoft Identity Web (if used in further views)
ms_identity_web = settings.MS_IDENTITY_WEB

def index_redirect(request):
    """
    Redirects the root URL to the 'index' view using a named URL pattern.
    """
    return redirect('index')  # Using named URL pattern for better maintainability


def index(request):
    """
    Renders the login page located at 'system_management/login.html'.
    """
    return render(request, 'system_management/login.html')


@ms_identity_web.login_required
def auth_redirect(request):
    """
    Redirects the logged in user to the claims page.
    """
    user_full_name = request.identity_context_data.username
    first_name, last_name = user_full_name.split(" ", 1)

    user_email_str = request.identity_context_data._token_cache
    try:
        user_email_dict = json.loads(user_email_str)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON data")

    user_email = None
    for key, value in user_email_dict.get("Account", {}).items():
        if "username" in value:
            user_email = value["username"]
            break
    else:
        return HttpResponseBadRequest("Error getting user email")

    User = get_user_model()
    password = make_password("root", hasher='default')  # Moved password generation to be inside the logic it's needed.

    if not User.objects.filter(email=user_email).exists():
        User.objects.create(
            email=user_email, 
            first_name=first_name, 
            last_name=last_name, 
            password=password
        )
    
    return redirect('claims')

def download_pdf(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'docs/final_user_manual.pdf')
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="calylocations_manual.pdf"'
    return response
