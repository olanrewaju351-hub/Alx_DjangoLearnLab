from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        url = reverse('post-list')  # registered by router -> 'post-list'
        data = {'title': 'API Post', 'content': 'content here'}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)

