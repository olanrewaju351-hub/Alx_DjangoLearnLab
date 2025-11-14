"""
settings.py — cleaned, secure, and environment-driven configuration
Drop this into LibraryProject/LibraryProject/settings.py (replace existing content or merge carefully).
"""

import os
from pathlib import Path

# -----------------------
# BASE
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------
# Helpers
# -----------------------
def env_bool(name, default=False):
    """Return True if environment variable name represents a true-like value."""
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes")

def env_int(name, default=0):
    try:
        return int(os.environ.get(name, str(default)))
    except (TypeError, ValueError):
        return default

# -----------------------
# SECRET / DEBUG / HOSTS
# -----------------------
# SECRET_KEY must come from environment in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or 'django-insecure-dev-fallback-change-me'
ECRET_KEY ='6SurBMU13evmhpLtmKjPRs2uA357ScQ2IzAcrBiEQBVh31sF4a6r7iLddGy5MQY-API'

# DEBUG default is False. Use DJANGO_DEBUG=1 or "True" for local dev.
DEBUG = env_bool('DJANGO_DEBUG', True)

# ALLOWED_HOSTS from env; default to localhost for dev
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# -----------------------
# INSTALLED APPS
# -----------------------
INSTALLED_APPS = [
    # Django contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'bookshelf',
    'relationship_app',
    'accounts',
]

# Optional: add django-csp when needed
if env_bool('DJANGO_USE_CSP', False):
    INSTALLED_APPS.append('csp')

# -----------------------
# MIDDLEWARE
# -----------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',            # important for many security settings
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Insert CSP middleware near the top if enabled
if 'csp' in INSTALLED_APPS and env_bool('DJANGO_USE_CSP', False):
    MIDDLEWARE.insert(1, 'csp.middleware.CSPMiddleware')

# -----------------------
# AUTH
# -----------------------
AUTH_USER_MODEL = 'accounts.CustomUser'  # keep if you have this custom user model

# -----------------------
# TEMPLATES
# -----------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -----------------------
# DATABASE (simple dev default)
# -----------------------
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DJANGO_DB_NAME', str(BASE_DIR / 'db.sqlite3')),
        # For Postgres/MySQL in production, set DJANGO_DB_* env vars and adjust the keys above.
    }
}

# -----------------------
# STATIC & MEDIA
# -----------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT', str(BASE_DIR / 'static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('DJANGO_MEDIA_ROOT', str(BASE_DIR / 'media'))

# -----------------------
# SECURITY: HTTPS, HSTS, Cookies, Headers
# -----------------------
# Decide SSL redirect via environment (True in production)
SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', True)

# HSTS: default to 1 year (31536000). Staged rollout recommended.
SECURE_HSTS_SECONDS = env_int('DJANGO_SECURE_HSTS_SECONDS', 31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', True)
SECURE_HSTS_PRELOAD = env_bool('DJANGO_SECURE_HSTS_PRELOAD', False)  # set True only when ready

# Cookies: only sent over HTTPS (set via env)
SESSION_COOKIE_SECURE = env_bool('DJANGO_SECURE_COOKIES', True)
CSRF_COOKIE_SECURE = env_bool('DJANGO_SECURE_COOKIES', True)

# HttpOnly flags
SESSION_COOKIE_HTTPONLY = True
# Keep CSRF cookie readable by JS unless your frontend requires it hidden
CSRF_COOKIE_HTTPONLY = False

# Browser protections
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# If behind a trusted reverse proxy that sets X-Forwarded-Proto:
# Example: SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
if env_bool('DJANGO_USE_PROXY_SSL_HEADER', False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -----------------------
# CSP (optional placeholders)
# -----------------------
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # avoid 'unsafe-inline' if possible
CSP_FONT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:")

# -----------------------
# Internationalization / Timezone (defaults)
# -----------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------
# Logging (basic)
# -----------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
    },
}

# -----------------------
# DEFAULT PRIMARY KEY TYPE
# -----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------
# LOGIN / REDIRECTS
# -----------------------
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/admin/login/'

# -----------------------
# Any additional app-specific settings can go below
# -----------------------

if env_bool('DJANGO_ALLOW_ALL_HOSTS', False):
    ALLOWED_HOSTS = ['*']

