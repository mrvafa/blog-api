from io import BytesIO

import requests
from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from Validators.image_validators import _is_image_width_less_than_or_equal, _is_image_height_less_than_or_equal, \
    _is_image_width_more_than_or_equal, _is_image_height_more_than_or_equal, _is_image_size_is_less_than_or_equal, \
    _is_allowed_extension, profile_image_validate


class TestImagePropertiesValidator(TestCase):
    def test_ok_min_width(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        im = Image.open(BytesIO(image_content))
        self.assertTrue(_is_image_width_less_than_or_equal(im, 200))

    def test_wrong_min_width(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        im = Image.open(BytesIO(image_content))
        self.assertFalse(_is_image_width_less_than_or_equal(im, 100))

    def test_ok_max_width(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        im = Image.open(BytesIO(image_content))
        self.assertTrue(_is_image_width_more_than_or_equal(im, 200))

    def test_wrong_max_width(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        im = Image.open(BytesIO(image_content))
        self.assertFalse(_is_image_width_more_than_or_equal(im, 1000))

    def test_ok_min_height(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        im = Image.open(BytesIO(image_content))
        self.assertTrue(_is_image_height_less_than_or_equal(im, 300))

    def test_wrong_min_height(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        im = Image.open(BytesIO(image_content))
        self.assertFalse(_is_image_height_less_than_or_equal(im, 250))

    def test_ok_max_height(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        im = Image.open(BytesIO(image_content))
        self.assertTrue(_is_image_height_more_than_or_equal(im, 300))

    def test_wrong_max_height(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        im = Image.open(BytesIO(image_content))
        self.assertFalse(_is_image_height_more_than_or_equal(im, 500))

    def test_ok_image_size_is_less_than_or_equal(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        self.assertTrue(_is_image_size_is_less_than_or_equal(image, 5))

    def test_wrong_image_size_is_less_than_or_equal(self):
        image_content = requests.get('https://picsum.photos/2000/3000').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        self.assertFalse(_is_image_size_is_less_than_or_equal(image, 0.0005))

    def test_ok_allowed_extension(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        self.assertTrue(_is_allowed_extension(image, ['jpg']))

    def test_wrong_allowed_extension(self):
        image_content = requests.get('https://picsum.photos/200/300').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        self.assertFalse(_is_allowed_extension(image, ['png']))


class TestImageValidator(TestCase):
    def test_ok_profile_image(self):
        image_content = requests.get(
            f'https://picsum.photos/{settings.PROFILE_IMAGE_WIDTH_MIN}/{settings.PROFILE_IMAGE_HEIGHT_MIN}').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        self.assertIsNone(profile_image_validate(image))

    def test_wrong_max_width_profile_image(self):
        image_content = requests.get(f'https://picsum.photos/{settings.PROFILE_IMAGE_WIDTH_MAX * 2}/'
                                     f'{settings.PROFILE_IMAGE_HEIGHT_MIN}').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        with self.assertRaises(ValidationError):
            profile_image_validate(image)

    def test_wrong_max_height_profile_image(self):
        image_content = requests.get(f'https://picsum.photos/{settings.PROFILE_IMAGE_WIDTH_MIN}/'
                                     f'{settings.PROFILE_IMAGE_HEIGHT_MAX * 2}').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        with self.assertRaises(ValidationError):
            profile_image_validate(image)

    def test_wrong_min_width_profile_image(self):
        image_content = requests.get(f'https://picsum.photos/{settings.PROFILE_IMAGE_WIDTH_MIN // 2}/'
                                     f'{settings.PROFILE_IMAGE_HEIGHT_MIN}').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        with self.assertRaises(ValidationError):
            profile_image_validate(image)

    def test_wrong_min_height_profile_image(self):
        image_content = requests.get(f'https://picsum.photos/{settings.PROFILE_IMAGE_WIDTH_MIN}/'
                                     f'{settings.PROFILE_IMAGE_HEIGHT_MIN // 2}').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        with self.assertRaises(ValidationError):
            profile_image_validate(image)

    def test_wrong_size_profile_image(self):
        image_content = requests.get(
            f'https://picsum.photos/{settings.PROFILE_IMAGE_WIDTH_MIN}/{settings.PROFILE_IMAGE_HEIGHT_MIN}').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        # for debugging
        tmp_image_max_size, settings.PROFILE_IMAGE_SIZE_MAX = settings.PROFILE_IMAGE_SIZE_MAX, 0
        with self.assertRaises(ValidationError):
            profile_image_validate(image)
        settings.PROFILE_IMAGE_SIZE_MAX = tmp_image_max_size

    def test_wrong_extension_profile_image(self):
        image_content = requests.get(
            f'https://picsum.photos/{settings.PROFILE_IMAGE_WIDTH_MIN}/{settings.PROFILE_IMAGE_HEIGHT_MIN}').content
        image = SimpleUploadedFile(
            name='test_image',
            content_type='image/jpeg',
            content=image_content,
        )
        # for debugging
        list_of_allowed_extension, settings.PROFILE_ALLOWED_IMAGE_EXTENSIONS = settings.PROFILE_IMAGE_SIZE_MAX, ['png']
        with self.assertRaises(ValidationError):
            profile_image_validate(image)
        settings.PROFILE_IMAGE_SIZE_MAX = list_of_allowed_extension
