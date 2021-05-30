import time

import requests
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from MyUser.models import User
from Post.models import Post
from Tag.models import Tag


class TestPost(TestCase):
    @staticmethod
    def _create_post_from_online_image(title, body, author, height=settings.POST_IMAGE_HEIGHT_MIN):
        image_content = requests.get(f'https://picsum.photos/{height}').content
        image = SimpleUploadedFile(
            name='test_post',
            content_type='image/jpeg',
            content=image_content,
        )
        post = Post.objects.create(title=title, author=author, body=body, image=image)
        return post

    def setUp(self):
        self.author = User.objects.create(username='user1')
        self.author.user_permissions.add(Permission.objects.get(codename='is_author'))

    def test_ok_create_post_title_body_image(self):
        TestPost._create_post_from_online_image('title 1', 'body', author=self.author)
        self.assertEqual('title-1', Post.objects.first().slug)

    def test_wrong_create_post_not_author(self):
        user = User.objects.create(username='user2', email='username@domain.com')
        with self.assertRaises(ValidationError):
            TestPost._create_post_from_online_image('title 2', 'body', author=user)

    def test_ok_create_check_added_time(self):
        post_before_created_datetime = timezone.now()
        TestPost._create_post_from_online_image(title='title 3', body='body 3', author=self.author)
        self.assertLessEqual(post_before_created_datetime, Post.objects.get(slug='title-3').added_datetime)

    def test_ok_create_title_check_modify_datetime(self):
        post = TestPost._create_post_from_online_image(title='title 4', body='body 4', author=self.author)
        time.sleep(1)
        post.body = 'text for body'
        post_modify_datetime = timezone.now()
        self.assertNotEqual(post.modify_datetime, post.added_datetime)
        self.assertLess(post.added_datetime, post_modify_datetime)
        self.assertGreaterEqual(post_modify_datetime, post.modify_datetime)

    def test_wrong_change_title(self):
        post = TestPost._create_post_from_online_image(title='title 5', body='body 5', author=self.author)
        post.title = ''
        with self.assertRaises(ValidationError):
            post.save()

    def test_wrong_change_body(self):
        post = TestPost._create_post_from_online_image(title='title 6', body='body 6', author=self.author)
        post.body = ''
        with self.assertRaises(ValidationError):
            post.save()

    def test_ok_add_tag(self):
        post = TestPost._create_post_from_online_image(title='title 7', body='body 7', author=self.author)
        tag = Tag.objects.create(title='tag 1')
        post.tags.add(tag)
        post.save()
        self.assertEqual(tag, Post.objects.get(slug='title-7').tags.first())

    def test_ok_add_tags(self):
        post = TestPost._create_post_from_online_image(title='title 8', body='body 8', author=self.author)
        tags = set()
        for i in range(10):
            tag = Tag.objects.create(title=f'tag {i}')
            post.tags.add(tag)
            tags.add(tag)
        post.save()
        self.assertEqual(tags, set(Post.objects.get(slug='title-8').tags.all()))
