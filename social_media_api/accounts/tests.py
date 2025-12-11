# accounts/tests.py
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

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

