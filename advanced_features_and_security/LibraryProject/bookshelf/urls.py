from django.urls import path, include
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('book/<int:pk>/', views.detail_book, name='detail_book'),
    path('bookshelf/', include('bookshelf.urls')),

]

