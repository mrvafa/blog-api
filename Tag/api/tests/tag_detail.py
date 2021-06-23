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
class TestDetailOfTag(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='mrvafa', )
        author_permission = Permission.objects.get(codename='is_author')
        self.user.user_permissions.add(author_permission)
        height = settings.POST_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{height}').content
        image = SimpleUploadedFile(
            name='test_post.png',
            content_type='image/jpeg',
            content=image_content,
        )
        self.post_1 = Post.objects.create(title='p1', image=image, author=self.user, body='b1')

        self.tag_1 = Tag.objects.create(title='t1', )
        self.tag_2 = Tag.objects.create(title='t2', )
        self.tag_3 = Tag.objects.create(title='t3', )

        self.post_1.tags.add(self.tag_1)
        self.post_1.tags.add(self.tag_2)
        self.post_1.tags.add(self.tag_3)

    def test_ok_detail_of_tag(self):
        respond = self.client.get(reverse('tag_detail', args=('t1',)))
        self.assertEqual(200, respond.status_code)
        self.assertEqual(self.tag_1.slug, respond.json()['slug'])

    def test_wrong_put_tag(self):
        respond = self.client.patch(reverse('tag_detail', args=('t1',)))
        self.assertEqual(405, respond.status_code)

    def test_ok_check_list_of_posts(self):
        respond = self.client.get(reverse('tag_detail', args=('t1',)))
        self.assertNotEqual([], respond.json()['posts'])

        respond = self.client.get(reverse('tag_detail', args=('t2',)))
        self.assertNotEqual([], respond.json()['posts'])

        respond = self.client.get(reverse('tag_detail', args=('t3',)))
        self.assertNotEqual([], respond.json()['posts'])
