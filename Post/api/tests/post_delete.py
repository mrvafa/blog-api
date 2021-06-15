import requests
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User
from Post.models import Post
from Tag.models import Tag


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class DeletePost(TestCase):
    def setUp(self):
        self.client = APIClient()
        author_permission = Permission.objects.get(codename='is_author')

        self.author_1 = User.objects.create(username='author1', )
        self.author_1.set_password('uR&w\'jC9`475f[~e')
        self.author_1.user_permissions.add(author_permission)
        self.author_1.save()

        self.author_2 = User.objects.create(username='author2', )
        self.author_2.set_password('tg!9MWt[EdV:_H#t')
        self.author_2.user_permissions.add(author_permission)
        self.author_2.is_superuser = True
        self.author_2.is_staff = True
        self.author_2.save()

        self.author_3 = User.objects.create(username='author3', )
        self.author_3.set_password('hWGK!L4+Y)V9K:;-')
        self.author_3.user_permissions.add(author_permission)
        self.author_3.save()

        self.author_1_token = self.client.post(
            reverse('rest_login'), data={'username': 'author1', 'password': 'uR&w\'jC9`475f[~e'}
        ).json()['key']

        self.author_2_token = self.client.post(
            reverse('rest_login'), data={'username': 'author2', 'password': 'tg!9MWt[EdV:_H#t'}
        ).json()['key']

        self.author_3_token = self.client.post(
            reverse('rest_login'), data={'username': 'author3', 'password': 'hWGK!L4+Y)V9K:;-'}
        ).json()['key']

        height = settings.POST_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{height}').content
        image = SimpleUploadedFile(
            name='test_post.png',
            content_type='image/jpeg',
            content=image_content,
        )
        self.tag_1 = Tag.objects.create(title='t1')

        self.post_1 = Post.objects.create(title='p1', image=image, author=self.author_1, body='b1')
        self.post_1.tags.add(self.tag_1)
        self.post_1.save()
        self.post_2 = Post.objects.create(title='p2', image=image, author=self.author_1, body='b2')
        self.post_3 = Post.objects.create(title='p3', image=image, author=self.author_3, body='b3')

    def test_ok_delete_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_1_token}')
        respond = self.client.get(reverse('post_destroy', args=('p1',)))
        self.assertEqual(200, respond.status_code)
        respond = self.client.delete(reverse('post_destroy', args=('p1',)))
        self.assertEqual(204, respond.status_code)

    def test_ok_delete_post_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_2_token}')
        respond = self.client.delete(reverse('post_destroy', args=('p1',)), )
        self.assertEqual(204, respond.status_code)

    def test_wrong_delete_post_non_owner_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_3_token}')
        respond = self.client.delete(reverse('post_destroy', args=('p2',)), )
        self.assertEqual(204, respond.status_code)
