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

class FollowFeedTests(APITestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(username='a', password='pass')
        self.user_b = User.objects.create_user(username='b', password='pass')
        self.post_b = Post.objects.create(author=self.user_b, title='B post', content='x')
        self.client.login(username='a', password='pass')

    def test_follow_and_feed(self):
        # follow user_b
        resp = self.client.post(reverse('follow-user', kwargs={'user_id': self.user_b.id}))
        self.assertEqual(resp.status_code, 200)

        # get feed
        resp = self.client.get(reverse('user-feed'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # paginated response: data['results'] contains posts
        self.assertTrue(any(p['id'] == self.post_b.id for p in data.get('results', [])))
