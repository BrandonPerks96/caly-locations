"""
WSGI config for proj_claims project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()

settings_module = 'app.settings.nonprod' if 'WEBSITE_HOSTNAME' in os.environ else 'app.settings.production'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()