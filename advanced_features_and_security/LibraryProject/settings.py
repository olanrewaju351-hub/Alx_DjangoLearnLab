import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Enforce HTTPS redirects
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Security headers
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# If behind a proxy/load balancer
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes")

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')  # no default in prod
if not SECRET_KEY:
    # fallback for local dev; DO NOT use in production
    SECRET_KEY = '6SurBMU13evmhpLtmKjPRs2uA357ScQ2IzAcrBiEQBVh31sF4a6r7iLddGy5MQY-API'

# DEBUG: default to False for safety; enable in dev via env var
DEBUG = env_bool('DJANGO_DEBUG', False)

# Hosts - set explicitly in production
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Force SSL redirect (enable in production when HTTPS is available)
SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', True)

# HSTS — enable only when using HTTPS and you understand implications.
# Example: one year (31536000) is common once you're ready.
SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', 31536000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', True)
SECURE_HSTS_PRELOAD = env_bool('DJANGO_SECURE_HSTS_PRELOAD', False)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Cookies only over HTTPS
SESSION_COOKIE_SECURE = env_bool('DJANGO_SECURE_COOKIES', True)
CSRF_COOKIE_SECURE = env_bool('DJANGO_SECURE_COOKIES', True)

# HttpOnly is safe for session cookie; CSRF cookie typically needs to be readable by JS in some setups
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False

# If you run behind a proxy (e.g. nginx, AWS ELB), set:
# (Only set this if your proxy sets X-Forwarded-Proto properly)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Base dir (single canonical definition)
BASE_DIR = Path(__file__).resolve().parent.parent

# Helper to read booleans from environment
def env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes")

# INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bookshelf',
    'relationship_app',
    'accounts',
]

# If you use django-csp, add it here (safe because INSTALLED_APPS exists)
if env_bool('DJANGO_USE_CSP', False):
    INSTALLED_APPS += ['csp']

# Custom user model (keep this if you have accounts.CustomUser)
AUTH_USER_MODEL = 'accounts.CustomUser'

# Secret key (use env var in production)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-development-key')

# DEBUG controlled from environment (default True for local dev)
DEBUG = env_bool('DJANGO_DEBUG', True)

# ALLOWED_HOSTS (environment driven)
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Security flags (use env vars; defaults suited for local dev)
SECURE_COOKIES = env_bool('DJANGO_SECURE_COOKIES', False)
SESSION_COOKIE_SECURE = SECURE_COOKIES
CSRF_COOKIE_SECURE = SECURE_COOKIES

# HttpOnly
SESSION_COOKIE_HTTPONLY = True
# Django expects CSRF cookie readable by JS for some front-end setups; keep False unless you know otherwise
CSRF_COOKIE_HTTPONLY = False

# Browser-side protections (defaults)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# SSL redirect & HSTS (use env vars; do NOT enable HSTS or SSL redirect until behind HTTPS in prod)
SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', False)
SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', 0))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
SECURE_HSTS_PRELOAD = env_bool('DJANGO_SECURE_HSTS_PRELOAD', False)

# Content-Security-Policy (only used if django-csp is installed & enabled)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # avoid 'unsafe-inline' if possible
CSP_FONT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:")

# Middleware - ensure CSP middleware is included if CSP is enabled
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if 'csp' in INSTALLED_APPS and env_bool('DJANGO_USE_CSP', False):
    # insert CSP middleware early (SecurityMiddleware should come before it)
    MIDDLEWARE.insert(1, 'csp.middleware.CSPMiddleware')

# Media (single BASE_DIR used above via pathlib.Path)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Login redirect
LOGIN_REDIRECT_URL = '/'

# For local development you can allow all hosts; in production set ALLOWED_HOSTS properly
if env_bool('DJANGO_ALLOW_ALL_HOSTS', False):
    ALLOWED_HOSTS = ['*']

