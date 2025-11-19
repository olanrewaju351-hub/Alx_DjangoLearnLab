# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
# register the viewset as requested
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # keep the old ListAPIView route if you still want it
    path('books/', BookList.as_view(), name='book-list'),

    # include all router-generated routes (list, create, retrieve, update, destroy, etc.)
    path('', include(router.urls)),
]

