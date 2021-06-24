from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
import requests

from MyUser.models import User
from Post.models import Post


class TestListOfPosts(TestCase):
    def setUp(self):
        self.client = APIClient()
        height = settings.POST_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{height}').content
        self.image = SimpleUploadedFile(
            name='test_post',
            content_type='image/jpeg',
            content=image_content,
        )
        self.user = User.objects.create(username='user')
        author_permission = Permission.objects.get(codename='is_author')
        self.user.user_permissions.add(author_permission)
        self.post_1 = Post.objects.create(title='p1', image=self.image, body='b1', author=self.user)
        self.post_2 = Post.objects.create(title='p2', image=self.image, body='b2', author=self.user)
        self.post_3 = Post.objects.create(title='p3', image=self.image, body='b3', author=self.user)

    def test_ok_list_of_tags(self):
        respond = self.client.get(reverse('post_list'))
        self.assertEqual(200, respond.status_code)

    def test_ok_list_of_tags_check_ordering(self):
        respond = self.client.get(reverse('post_list'))
        posts = respond.json()['results']
        self.assertEqual('p3', posts[0]['title'])
        self.assertEqual('p2', posts[1]['title'])
        self.assertEqual('p1', posts[2]['title'])

    def test_ok_search_in_title(self):
        respond = self.client.get(reverse('post_list') + '?search=p1')
        posts = respond.json()['results']
        self.assertEqual(1, len(posts))
        self.assertEqual('p1', posts[0]['title'])
