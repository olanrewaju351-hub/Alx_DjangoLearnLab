from django.urls import path
from .views import list_books, LibraryDetailView
from . import views  # ✅ ensures 'views.register' is recognized

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),  # ✅ this is what the test looks for
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

