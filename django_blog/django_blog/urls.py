# django_blog/urls.py (cleaned & standardized)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth / account routes (namespaced in accounts/urls.py)
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # Main blog app at site root (namespaced in blog/urls.py)
    # Ensure blog/urls.py defines app_name = 'blog' or uses the same namespace.
    path('', include(('blog.urls', 'blog'), namespace='blog')),

    # Add other app includes below, e.g.
    # path('shop/', include(('shop.urls', 'shop'), namespace='shop')),
]

# Development-only: serve media files uploaded by users (DEBUG=True)
# Note: runserver serves app/static files automatically; you normally don't need to
# add static(settings.STATIC_URL...) here. STATIC_ROOT is for collectstatic in production.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

