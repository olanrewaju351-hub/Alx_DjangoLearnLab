Security hardening notes
------------------------
1. DEBUG controlled via DJANGO_DEBUG environment variable.
2. Cookie security: CSRF_COOKIE_SECURE & SESSION_COOKIE_SECURE set in production.
3. Browser security: SECURE_BROWSER_XSS_FILTER, X_FRAME_OPTIONS, SECURE_CONTENT_TYPE_NOSNIFF enabled.
4. CSP: enabled via django-csp middleware (see settings).
5. All forms include {% csrf_token %} and use Django Forms for validation.
6. Views use Django ORM (no raw SQL). Sensitive views are protected by @permission_required.
7. Test checklist included: CSRF/XSS/SQLi/CSP/cookie checks.

