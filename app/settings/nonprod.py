from .base import *
from .base import BASE_DIR
from azure.identity import DefaultAzureCredential
import logging
import os
 
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
 
logger = logging.getLogger(__name__)
 
DEBUG = False
logger.debug(f'DEBUG mode is set to: {DEBUG}')
 
DEBUG_PROPAGATE_EXCEPTIONS = True
 
ALLOWED_HOSTS = ['lwasanappnonprod.azurewebsites.net']
logger.debug(f'ALLOWED_HOSTS is set to: {ALLOWED_HOSTS}')
 
CSRF_TRUSTED_ORIGINS = ['https://lwasanappnonprod.azurewebsites.net']
logger.debug(f'CSRF_TRUSTED_ORIGINS is set to: {CSRF_TRUSTED_ORIGINS}')
 
 
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'ms_identity_web.django.middleware.MsalMiddleware',
]
 
 
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
 
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
 
# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'USER': '',
        'PASSWORD': '',
        'PORT': 1433,
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': f'Authentication=ActiveDirectoryMsi;UID={os.getenv("UID")};',
        }
    }
}


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')