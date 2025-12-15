import os
import environ
from pathlib import Path
# BASE_DIR is typically defined here by Django
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Load Environment Variables ---
env = environ.Env()

# Look for the .env file one directory up 
if os.path.exists(BASE_DIR.parent / '.env'):
    environ.Env.read_env(env_file=str(BASE_DIR.parent / '.env'))

# --- Apply Core Settings ---
SECRET_KEY = env('SECRET_KEY')
# Use env.bool() to safely cast "True"/"False" strings to Python booleans
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',                  
    'rest_framework_simplejwt',        
    'authentication.apps.AuthenticationConfig',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"

AUTH_USER_MODEL = 'authentication.User'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": env.db()
}

if not DATABASES['default']:
    raise Exception("DATABASE_URL not found or invalid in environment.")


# --- DRF Global Configuration ---
REST_FRAMEWORK = {
    # Default Authentication: Require a valid JWT token
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Default Permissions: All API views require authentication
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Use DRF filters for search/ordering
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

# --- SIMPLE_JWT Configuration (The Token Standard) ---
from datetime import timedelta
SIMPLE_JWT = {
    # JWT signing key is pulled from the .env file
    "SIGNING_KEY": env('SIMPLE_JWT_SIGNING_KEY'),
    
    # Token life for professional standard (30-60 minutes)
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    
    # Ensures the frontend uses the standard "Authorization: Bearer <token>" header
    "AUTH_HEADER_TYPES": ("Bearer",),
    
    # Use standard user model fields for token subjects
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
