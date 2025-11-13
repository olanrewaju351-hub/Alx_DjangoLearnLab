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

AUTH_USER_MODEL = 'accounts.CustomUser'

# SECURITY: do NOT run with DEBUG=True in production.
# Use environment variable to toggle in real deployments.
import os
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# Recommended: explicitly set allowed hosts in production
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# === Browser protections ===
# Enable browser XSS filter
SECURE_BROWSER_XSS_FILTER = True

# Prevent the site from being framed (mitigates clickjacking)
X_FRAME_OPTIONS = "DENY"   # or "SAMEORIGIN" if you need embedding from same origin

# Prevent content type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Ensure cookies are only sent over HTTPS in production
CSRF_COOKIE_SECURE = os.environ.get("DJANGO_SECURE_COOKIES", "False") == "True"
SESSION_COOKIE_SECURE = os.environ.get("DJANGO_SECURE_COOKIES", "False") == "True"

# Use HttpOnly to prevent JS access to cookies
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # Django expects CSRF cookie accessible to JS for some setups; keep False unless you use other strategies

# HSTS (only enable in production after verifying HTTPS)
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", 0))  # e.g. 31536000 for 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

# Use secure SSL redirect in production
SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "False") == "True"

# Content Security Policy (if using django-csp, see below)
# Example fallback default (will be set by middleware or django-csp settings)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # avoid 'unsafe-inline' if possible

INSTALLED_APPS += ['csp']  # or insert in the list
MIDDLEWARE = [
    # ... existing middleware ...
    'csp.middleware.CSPMiddleware',
    # ... remaining middleware ...
]

# Example CSP rules — tighten as needed
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "https://cdnjs.cloudflare.com")   # allow CDNs you trust
CSP_STYLE_SRC = ("'self'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:")


# Media (for development)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/'

ALLOWED_HOSTS = ['*']

