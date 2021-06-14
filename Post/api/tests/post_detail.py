import requests
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User
from Post.models import Post


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestDetailOfPost(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='mrvafa', )
        author_permission = Permission.objects.get(codename='is_author')
        self.user.user_permissions.add(author_permission)
        height = settings.POST_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{height}').content
        image = SimpleUploadedFile(
            name='test_post',
            content_type='image/jpeg',
            content=image_content,
        )
        self.post_1 = Post.objects.create(title='p1', image=image, author=self.user, body='b1')
        self.post_2 = Post.objects.create(title='p2', image=image, author=self.user, body='b2')
        self.post_3 = Post.objects.create(title='p3', image=image, author=self.user, body='b3')

    def test_ok_detail_of_post(self):
        respond = self.client.get(reverse('post_detail', args=('p1',)))
        self.assertEqual(200, respond.status_code)
        self.assertEqual(self.post_1.slug, respond.json()['slug'])

    def test_wrong_put_post(self):
        respond = self.client.patch(reverse('post_detail', args=('p1',)))
        self.assertEqual(405, respond.status_code)
