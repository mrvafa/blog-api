import os
import time

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from Tag.models import Tag


class TestTag(TestCase):
    def test_ok_create_title(self):
        tag = Tag.objects.create(title='tag_1')
        self.assertEqual(tag, Tag.objects.get(title='tag_1'))

    def test_ok_create_title_check_slug(self):
        Tag.objects.create(title='tag_1')
        self.assertEqual('tag_1', Tag.objects.get(slug='tag_1').slug)

    def test_ok_create_title_check_added_time(self):
        tag_before_created_datetime = timezone.now()
        Tag.objects.create(title='tag_1')
        self.assertLessEqual(tag_before_created_datetime, Tag.objects.get(slug='tag_1').added_datetime)

    def test_ok_create_title_check_modify_datetime(self):
        tag = Tag.objects.create(title='tag_1')
        time.sleep(1)
        tag.body = 'text for body'
        tag_modify_datetime = timezone.now()
        self.assertNotEqual(tag.modify_datetime, tag.added_datetime)
        self.assertLess(tag.added_datetime, tag_modify_datetime)
        self.assertGreaterEqual(tag_modify_datetime, tag.modify_datetime)

    def test_ok_create_title_body(self):
        tag = Tag.objects.create(title='tag_2', body='This is a body')
        self.assertEqual(tag.body, Tag.objects.first().body)

    def test_ok_create_title_body_image(self):
        height = settings.TAG_IMAGE_HEIGHT_MIN
        image_content = requests.get(f'https://picsum.photos/{height}').content
        image = SimpleUploadedFile(
            name='test_tag',
            content_type='image/jpeg',
            content=image_content,
        )
        Tag.objects.create(title='tag_3', body='This is a body', image=image)

        saved_image_path = Tag.objects.get(title='tag_3').image.name
        saved_image_name = os.path.basename(saved_image_path)
        self.assertTrue(saved_image_name.startswith(image.name))

    def test_ok_change_title(self):
        tag = Tag.objects.create(title='tag_4')
        tag.title = 'tag_4_1'
        tag.save()
        self.assertEqual('tag_4_1', Tag.objects.first().title)

    def test_ok_change_title_check_slug(self):
        tag = Tag.objects.create(title='tag 5')
        tag.title = 'tag 5 1'
        tag.save()
        self.assertEqual('tag-5-1', Tag.objects.first().slug)

    def test_wrong_change_title(self):
        tag = Tag.objects.create(title='tag 5')
        tag.title = ''
        with self.assertRaises(ValidationError):
            tag.save()
