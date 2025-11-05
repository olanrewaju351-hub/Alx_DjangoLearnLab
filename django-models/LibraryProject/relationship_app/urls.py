from django.contrib import admin
from django.urls import path, include  # ✅ include is needed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),  # ✅ include the relationship_app URLs
]


