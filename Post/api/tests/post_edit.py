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
class TestEditPost(TestCase):
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
        self.author_2.is_staff = True
        self.author_2.is_superuser = True
        self.author_2.save()

        height = settings.POST_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{height}').content
        image = SimpleUploadedFile(
            name='test_post.png',
            content_type='image/jpeg',
            content=image_content,
        )

        self.tag_1 = Tag.objects.create(title='t1')
        self.tag_2 = Tag.objects.create(title='t2')
        self.tag_3 = Tag.objects.create(title='t3')

        self.post_1 = Post.objects.create(title='p1', image=image, author=self.author_1, body='b1')
        self.post_1.tags.add(self.tag_1)
        self.post_1.save()

        self.post_2 = Post.objects.create(title='p2', image=image, author=self.author_1, body='b2')
        self.post_2.tags.add(self.tag_2)
        self.post_2.tags.add(self.tag_3)
        self.post_2.save()

        self.post_3 = Post.objects.create(title='p3', image=image, author=self.author_2, body='b3')

        self.author_1_token = self.client.post(
            reverse('rest_login'), data={'username': 'author1', 'password': 'uR&w\'jC9`475f[~e'}
        ).json()['key']

        self.author_2_token = self.client.post(
            reverse('rest_login'), data={'username': 'author2', 'password': 'tg!9MWt[EdV:_H#t'}
        ).json()['key']

    def test_ok_get_edit_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_1_token}')
        respond = self.client.get(reverse('post_update', args=('p1',)))
        self.assertEqual(200, respond.status_code)
        self.assertEqual(self.post_1.slug, respond.json()['slug'])

    def test_ok_post_edit_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_1_token}')
        respond = self.client.patch(reverse('post_update', args=('p1',)), data={'body': 'hello'})
        self.assertEqual(200, respond.status_code)
        self.assertEqual('hello', respond.json()['body'])

    def test_ok_post_edit_post_add_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_1_token}')
        respond = self.client.patch(reverse('post_update', args=('p2',)), data={'tags': [self.tag_1.id]})
        self.assertEqual(200, respond.status_code)
        self.assertEqual(Post.objects.get(slug='p2').tags.first().id, respond.json()['tags'][0])

    def test_ok_post_edit_post_remove_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_1_token}')
        respond = self.client.patch(reverse('post_update', args=('p1',)), data={'tags': []})
        self.assertEqual(200, respond.status_code)
        self.assertIsNone(Post.objects.get(slug='p1').tags.first())

    def test_ok_post_edit_post_edit_image(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_1_token}')
        height = settings.POST_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{height}').content
        image = SimpleUploadedFile(
            name='replaced_image.png',
            content_type='image/jpeg',
            content=image_content,
        )
        respond = self.client.patch(reverse('post_update', args=('p2',)), data={'image': image})
        self.assertEqual(200, respond.status_code)
        self.assertIn('replaced_image', Post.objects.get(slug='p2').image.path)

    def test_wrong_edit_post_wrong_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_2_token}')
        respond = self.client.get(reverse('post_update', args=('p2',)))
        self.assertEqual(403, respond.status_code)

    def test_ok_post_edit_post_remove_one_of_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.author_1_token}')
        respond = self.client.patch(reverse('post_update', args=('p2',)), data={'tags': [self.tag_2.id]})
        self.assertEqual(200, respond.status_code)
        self.assertEqual(len(Post.objects.get(slug='p2').tags.all()), 1)
        self.assertEqual(Post.objects.get(slug='p2').tags.first(), Tag.objects.get(title='t2'))
