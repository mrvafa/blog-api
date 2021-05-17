import os.path
from datetime import datetime

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from Profile.models import Profile


def _create_two_user():
    user1 = User(username='user1')
    user1.set_password('gD!9zx%eYXTd@;X')
    user1.save()
    user2 = User(username='user2')
    user2.set_password('gD!9zx%eYXTd@;X')
    user2.save()
    return user1, user2


class TestProfile(TestCase):
    def test_create_profile_username_only(self):
        user = User(username='user1')
        user.set_password('gD!9zx%eYXTd@;X')
        user.save()

        Profile(user=user, ).save()

        self.assertEqual(1, len(Profile.objects.all()))

    def test_create_profile_gender(self):
        user = User(username='user1')
        user.set_password('gD!9zx%eYXTd@;X')
        user.save()

        Profile(user=user, gender='m').save()

        self.assertEqual(1, len(Profile.objects.all()))
        self.assertEqual('m', Profile.objects.first().gender)

    def test_create_profile_birthday(self):
        user = User(username='user1')
        user.set_password('gD!9zx%eYXTd@;X')
        user.save()

        Profile(user=user, birthday='1989-04-11').save()

        self.assertEqual(datetime(1989, 4, 11).date(), Profile.objects.first().birthday)

    def test_create_profile_phone_number(self):
        user1, user2 = _create_two_user()

        Profile(user=user1, phone_number='09132345678').save()
        Profile(user=user2, phone_number='+989132345679').save()

        self.assertEqual(
            '+989132345678', Profile.objects.first().phone_number
        )
        self.assertEqual(
            '+989132345679', Profile.objects.last().phone_number
        )

    def test_create_unique_profile_phone_number(self):
        user1, user2 = _create_two_user()

        Profile(user=user1, phone_number='09132345679').save()
        try:
            Profile(user=user2, phone_number='+989132345679').save()
            self.assertFalse('1')
        except ValidationError as e:
            self.assertEqual(
                'Profile with this Phone number already exists.', e.messages[0]
            )
            self.assertEqual(1, len(e.messages))

        self.assertEqual(1, len(Profile.objects.all()))

    def test_create_profile_image(self):
        user = User(username='user')
        user.set_password('gD!9zx%eYXTd@;X')
        user.save()

        profile = Profile(user=user, )
        profile.save()

        profile.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=requests.get(
                'https://d1nhio0ox7pgb.cloudfront.net/_img/v_collection_png/512x512/shadow/businessman.png').content,
            content_type='image/jpeg'
        )
        profile.save()

        self.assert_(os.path.isfile(profile.image.path))
        profile.delete()
        self.assert_(not os.path.isfile(profile.image.path))

    def test_create_set_image_profile(self):
        user = User(username='user')
        user.set_password('gD!9zx%eYXTd@;X')
        user.save()

        profile = Profile(user=user, )
        profile.save()

        number_of_images_before_creating_profiles = len(
            os.listdir(os.path.join(settings.MEDIA_ROOT, 'profile_images', f'{datetime.now().month:02}'))
        )
        url = 'https://donoghte.com/wp-content/uploads/2021/02/9ce9b71fecb95ae0a7ff94c36d0a9942-donoghte.com_.jpg'
        for _ in range(3):
            profile.set_profile_image(url)
        self.assertEqual(
            1 + number_of_images_before_creating_profiles,
            len(os.listdir(os.path.join(settings.MEDIA_ROOT, 'profile_images', f'{datetime.now().month:02}')))
        )
