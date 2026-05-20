from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ms_identity_web.django.msal_views_and_urls import MsalViews

# Generate URL patterns for Microsoft Identity Platform
msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()

# URL Configuration for the Django project
# See: https://docs.djangoproject.com/en/5.0/topics/http/urls/ for more information
urlpatterns = [
    path("admin/", admin.site.urls),  # Admin site
    path("", include("claims.urls")),  # Claims app URLs
    path("", include("system_management.urls")),  # System management app URLs
    path(f"{settings.AAD_CONFIG.django.auth_endpoints.prefix}/", include(msal_urls)),  # MSAL authentication URLs
    # path('sentry-debug/', trigger_error),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serving media files in development


# Examples of URL configurations:
# Function views:
#   1. Add an import: from my_app import views
#   2. Add a URL to urlpatterns: path('', views.home, name='home')
# Class-based views:
#   1. Add an import: from other_app.views import Home
#   2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
# Including another URLconf:
#   1. Import the include() function: from django.urls import include, path
#   2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
