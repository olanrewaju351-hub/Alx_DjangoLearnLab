# api/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Author, Book

User = get_user_model()

class BookAPITestCase(APITestCase):
    """
    Tests for Book API endpoints:
      - list (with filtering/search/ordering)
      - retrieve
      - create (auth required)
      - update (auth required)
      - delete (auth required)
    Assumes the following named URL patterns exist in api/urls.py:
      - 'book-list'      -> /api/books/
      - 'book-detail'    -> /api/books/<pk>/
      - 'book-create'    -> /api/books/create/
      - 'book-update'    -> /api/books/update/<pk>/
      - 'book-delete'    -> /api/books/delete/<pk>/
    If your URL names differ, change the reverse(...) calls below.
    """

    def setUp(self):
        # Create two users: a regular user and a staff user
        self.user = User.objects.create_user(username='regular', password='pass1234')
        self.staff_user = User.objects.create_user(username='staff', password='pass1234', is_staff=True)

        # API clients
        self.client = APIClient()                 # unauthenticated client
        self.auth_client = APIClient()            # will be force-authenticated as regular user
        self.auth_client.force_authenticate(user=self.user)
        self.staff_client = APIClient()           # will be force-authenticated as staff user
        self.staff_client.force_authenticate(user=self.staff_user)

        # Create sample author and books
        self.author = Author.objects.create(name='George Orwell')
        self.book1 = Book.objects.create(title='1984', publication_year=1949, author=self.author)
        self.book2 = Book.objects.create(title='Animal Farm', publication_year=1945, author=self.author)
        # additional book for ordering/filtering tests
        self.book3 = Book.objects.create(title='A Brave New World', publication_year=1932, author=self.author)

        # Named URLs (expects you used these names in api/urls.py)
        self.list_url = reverse('book-list')           # e.g., /api/books/
        self.create_url = reverse('book-create')       # e.g., /api/books/create/

    def test_list_books_returns_all(self):
        """GET /api/books/ should return list of books and 200 OK"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        # Expect at least the 3 sample books
        titles = [b['title'] for b in data]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)
        self.assertIn(self.book3.title, titles)

    def test_filter_by_publication_year(self):
        """Filtering by publication_year should return matching books"""
        response = self.client.get(self.list_url, {'publication_year': 1949})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], '1984')

    def test_search_by_title(self):
        """Search endpoint should support partial matching on title"""
        response = self.client.get(self.list_url, {'search': 'Animal'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Animal Farm')

    def test_ordering_by_publication_year(self):
        """Ordering should sort results by publication_year"""
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        years = [b['publication_year'] for b in data]
        # Check ascending ordering
        self.assertEqual(years, sorted(years))

        # descending
        response2 = self.client.get(self.list_url, {'ordering': '-publication_year'})
        data2 = response2.data
        years2 = [b['publication_year'] for b in data2]
        self.assertEqual(years2, sorted(years2, reverse=True))

    def test_retrieve_book_detail(self):
        """GET /api/books/<pk>/ returns individual book"""
        url = reverse('book-detail', args=[self.book1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['title'], '1984')
        self.assertEqual(data['publication_year'], 1949)
        # author is represented by id or nested representation depending on serializer
        self.assertTrue('author' in data)

    def test_create_book_requires_authentication(self):
        """Unauthenticated POST to create should be forbidden (401 or 403)"""
        payload = {'title': 'New Book', 'publication_year': 2020, 'author': self.author.id}
        response = self.client.post(self.create_url, payload, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """Authenticated user can create a book"""
        payload = {'title': 'New Book', 'publication_year': 2020, 'author': self.author.id}
        response = self.auth_client.post(self.create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertEqual(data['title'], 'New Book')
        self.assertEqual(data['publication_year'], 2020)

    def test_update_book_authenticated(self):
        """Authenticated user can update a book (PUT)"""
        url = reverse('book-update', args=[self.book1.pk])
        payload = {'title': '1984 - updated', 'publication_year': 1949, 'author': self.author.id}
        response = self.auth_client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, '1984 - updated')

    def test_partial_update_book_authenticated(self):
        """Authenticated user can partially update a book (PATCH)"""
        url = reverse('book-update', args=[self.book2.pk])
        payload = {'title': 'Animal Farm (edited)'}
        response = self.auth_client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, 'Animal Farm (edited)')

    def test_delete_book_requires_authentication(self):
        """Unauthenticated delete should fail"""
        url = reverse('book-delete', args=[self.book3.pk])
        response = self.client.delete(url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book"""
        url = reverse('book-delete', args=[self.book3.pk])
        response = self.auth_client.delete(url)
        # either 204 No Content (successful delete) or 200 depending on view; accept both
        self.assertIn(response.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        # verify object is gone
        exists = Book.objects.filter(pk=self.book3.pk).exists()
        self.assertFalse(exists)

    def test_delete_requires_staff_if_configured(self):
        """
        If your delete view restricts deletion to staff users, confirm that a regular
        authenticated user cannot delete while a staff user can.
        This test is tolerant: it passes if either deletion-by-authenticated is allowed,
        or if only staff can delete (regular gets 403 while staff deletes successfully).
        """
        url = reverse('book-detail', args=[self.book1.pk])  # fallback if delete route wasn't created
        # try regular user delete first on delete endpoint if available
        delete_url = None
        try:
            delete_url = reverse('book-delete', args=[self.book1.pk])
        except:
            delete_url = url  # maybe the delete uses the detail endpoint

        response_regular = self.auth_client.delete(delete_url)
        # if forbidden for regular user, ensure staff can delete
        if response_regular.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED):
            response_staff = self.staff_client.delete(delete_url)
            self.assertIn(response_staff.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        else:
            # regular user was allowed to delete; assert deletion happened
            self.assertIn(response_regular.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))

