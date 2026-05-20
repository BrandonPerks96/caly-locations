import os
from pathlib import Path
from dotenv import load_dotenv
from ms_identity_web import IdentityWebPython
from ms_identity_web.configuration import AADConfig
import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

# Load environment variables
load_dotenv()
 
# Base directory setup
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Azure Active Directory Configuration
AAD_CONFIG = AADConfig.parse_json(file_path='aad.config.json')

# Pass environment variables to AADConfig
AAD_CONFIG.client.client_id = os.getenv('CLIENT_ID')
AAD_CONFIG.client.client_credential = os.getenv('CLIENT_CRED')
AAD_CONFIG.client.authority = os.getenv('AUTHORITY_LOGIN')

MS_IDENTITY_WEB = IdentityWebPython(AAD_CONFIG)
ERROR_TEMPLATE = 'auth/{}.html'  # Template for error handling in MSAL middleware
 
# Application configuration settings
SECRET_KEY = os.environ.get('SECRET_KEY')
AUTH_USER_MODEL = 'system_management.CustomUser'
 
# Session settings
SESSION_COOKIE_AGE = 7200
SESSION_SAVE_EVERY_REQUEST = True
 
# CORS settings
CORS_ORIGIN_ALLOW_ALL = True

# Installed applications and middleware configuration
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "claims",
    "system_management",
    "django_extensions",
    "mathfilters",
]
CRISPY_TEMPLATE_PACK = "bootstrap5"
 
# URL and WSGI configuration
ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "app.wsgi.application"
 
# Template configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
 
# Password validation configuration
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "system_management.validators.super_user_password_validator.ComplexPasswordValidator",
    },
]
 
# Localization settings
LANGUAGE_CODE = "en-us"
USE_TZ = True
TIME_ZONE = "UTC"
USE_I18N = True
 
# API keys and other constants
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
 
# sentry_sdk.init(
#     dsn="https://9e8648fbccba072b551c134178461278@o4507684019568640.ingest.us.sentry.io/4507684224499712",
#     integrations=[DjangoIntegration()],
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     traces_sample_rate=1.0,
#     # Set profiles_sample_rate to 1.0 to profile 100%
#     # of sampled transactions.
#     # We recommend adjusting this value in production.
#     profiles_sample_rate=1.0,
#     send_default_pii=True  # Send default PII (PII = personally identifiable information)
# )
