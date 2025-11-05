from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # include relationship_app under the 'relationship/' prefix
    path('relationship/', include('relationship_app.urls', namespace='relationship_app')),
]


