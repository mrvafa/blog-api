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
class TestEditTag(TestCase):
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
        self.tag_1 = Tag.objects.create(title='t1', )
        self.tag_2 = Tag.objects.create(title='t2', )
        self.tag_3 = Tag.objects.create(title='t3', )

    def test_ok_edit_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_token}')
        respond = self.client.get(reverse('tag_update', args=('t1',)))
        self.assertEqual(200, respond.status_code)
        self.assertEqual(self.tag_1.slug, respond.json()['slug'])
        respond = self.client.put(reverse('tag_update', args=('t1',)), data={'title': 's5'})
        self.assertEqual(200, respond.status_code)
        self.assertIsNotNone(Tag.objects.filter(slug='s5'))

    def test_wrong_edit_tag_non_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        respond = self.client.put(reverse('tag_update', args=('t1',)), data={'title': 't5'})
        self.assertEqual(403, respond.status_code)

    def test_wrong_edit_tag_not_unique_title(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_token}')
        respond = self.client.put(reverse('tag_update', args=('t1',)), data={'title': 't2'})
        self.assertEqual(400, respond.status_code)

    def test_ok_tag_remove_image(self):
        width = settings.TAG_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{width}/').content
        image = SimpleUploadedFile(
            name='test_profile',
            content_type='image/jpeg',
            content=image_content,
        )
        self.tag_1.image = image
        self.tag_1.save()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_token}')
        respond = self.client.put(reverse('tag_update', args=('t1',)), data={'image': ''})
        self.assertEqual(200, respond.status_code)
        self.assertEqual('', Tag.objects.filter(slug='t1').first().image.name)

    def test_ok_tag_not_remove_image(self):
        width = settings.TAG_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{width}/').content
        image = SimpleUploadedFile(
            name='test_profile.jpg',
            content_type='image/jpeg',
            content=image_content,
        )
        self.tag_1.image = image
        self.tag_1.save()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_token}')
        respond = self.client.put(reverse('tag_update', args=('t1',)), data={'title': 'b31'})
        self.assertEqual(200, respond.status_code)
        self.assertNotEqual('', Tag.objects.filter(slug='b31').first().image.name)
