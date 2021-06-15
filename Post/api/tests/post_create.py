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
class TestCreatePost(TestCase):
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
        self.author_2.save()

        self.author_3 = User.objects.create(username='author3', )
        self.author_3.set_password('hWGK!L4+Y)V9K:;-')
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
        self.image = SimpleUploadedFile(
            name='test_profile.png',
            content_type='image/jpeg',
            content=image_content,
        )

    def test_ok_create_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_1_token}')
        data = {'title': 't1', 'body': 'b1', 'image': self.image}
        respond = self.client.post(reverse('post_create', ), data=data)
        self.assertEqual(201, respond.status_code)
        self.assertEqual(Post.objects.first().slug, respond.json()['slug'])

    def test_ok_create_post_check_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_1_token}')
        data = {'title': 't1', 'body': 'b1', 'image': self.image}
        respond = self.client.post(reverse('post_create'), data=data)
        self.assertEqual(self.author_1.username, respond.json()['author'])

    def test_ok_post_create_post_with_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_1_token}')
        tag = Tag.objects.create(title='t1')
        data = {'title': 't45', 'body': 'b45', 'image': self.image, 'tags': [tag.id]}
        respond = self.client.post(reverse('post_create', ), data=data)
        self.assertEqual(201, respond.status_code)
        self.assertEqual(Post.objects.first().tags.first().id, respond.json()['tags'][0])

    def test_wrong_create_post_non_author_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_3_token}')
        data = {'title': 't1', 'body': 'b1', 'image': self.image}
        respond = self.client.post(reverse('post_create', ), data=data)
        self.assertEqual(403, respond.status_code)
