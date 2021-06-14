import requests
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User
from Tag.models import Tag


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestCreateTag(TestCase):
    def setUp(self):
        self.client = APIClient()
        author_permission = Permission.objects.get(codename='is_author')
        self.author = User.objects.create(username='author')
        self.author.set_password('WZfP(m{F<=p87#8j')
        self.author.save()
        self.author.user_permissions.add(author_permission)
        respond = self.client.post(reverse('rest_login'), data={'username': 'author', 'password': 'WZfP(m{F<=p87#8j'})
        self.author_token = respond.json()['key']
        self.admin = User.objects.create(username='admin', is_staff=True)
        self.admin.set_password('-r&bVsCj,6LW#~..')
        self.admin.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'admin', 'password': '-r&bVsCj,6LW#~..'})
        self.admin_token = respond.json()['key']

    def test_ok_create_tag(self):
        data = {
            'title': 't1',
            'body': 'b1',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_token}')
        respond = self.client.post(reverse('tag_create'), data=data)
        self.assertEqual(201, respond.status_code)
        self.assertEqual(Tag.objects.get(slug='t1').slug, respond.json()['slug'])

    def test_wrong_put_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_token}')
        respond = self.client.patch(reverse('tag_create', ))
        self.assertEqual(405, respond.status_code)

    def test_wrong_post_slug(self):
        data = {
            'title': 't1',
            'body': 'b1',
            'slug': 'asf'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_token}')
        respond = self.client.post(reverse('tag_create'), data=data)
        self.assertEqual(201, respond.status_code)
        self.assertEqual(Tag.objects.get(slug='t1').slug, respond.json()['slug'])

    def test_wrong_non_author(self):
        data = {
            'title': 't1',
            'body': 'b1',
            'slug': 'asf'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        respond = self.client.post(reverse('tag_create'), data=data)
        self.assertEqual(403, respond.status_code)
        self.assertIsNone(Tag.objects.filter(slug='t1').first())

    def test_ok_create_tag_with_image(self):
        width = settings.TAG_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{width}/').content
        image = SimpleUploadedFile(
            name='test_post.jpg',
            content_type='image/jpeg',
            content=image_content,
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_token}', )
        respond = self.client.post(reverse('tag_create'), data={'title': 'b31', 'image': image}, )
        self.assertEqual(201, respond.status_code)
        self.assertNotEqual('', Tag.objects.filter(title='b31').first().image.name)
