# accounts/urls.py
from django.urls import path
from .views import RegisterView, CustomObtainAuthToken, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='account-register'),
    path('login/', CustomObtainAuthToken.as_view(), name='account-login'),
    path('profile/', ProfileView.as_view(), name='account-profile'),
]

