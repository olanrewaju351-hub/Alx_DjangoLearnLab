# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    # token auth endpoint (POST username & password -> returns token)
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # include router urls
    path('', include(router.urls)),
]

