import os

import requests
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from MyUser.models import User


class TestUser(TestCase):
    def test_create_ok_user_with_username_password(self):
        user = User.objects.create(username='user1', email='user1@domain.com')
        user.set_password('Ded+h}=_YF9Ppn,L')
        self.assertIsNotNone(User.objects.get(username='user1'))

    def test_create_ok_user_with_username_password_gender(self):
        user = User.objects.create(username='user2', email='user2@domain.com', gender='f')
        user.set_password('zu4,{$w~@YMP67Ac')
        self.assertIsNotNone(User.objects.get(username='user2'))

    def test_create_ok_user_with_username_password_gender_birthday(self):
        user = User.objects.create(username='user3', email='user3@domain.com', gender='m', birthday='2000-01-07')
        user.set_password('^\\KXY(8deX\'GM,h8')
        self.assertIsNotNone(User.objects.get(username='user3'))

    def test_create_ok_user_with_username_password_gender_birthday_phone_number(self):
        user = User.objects.create(
            username='user4',
            email='user4@domain.com',
            gender='m',
            birthday='2000-01-07',
            phone_number='+989123456789',
        )
        user.set_password('*YuF?AS6sCr4TQ`t')
        self.assertIsNotNone(User.objects.get(username='user4'))

    def test_create_ok_user_with_username_password_gender_birthday_phone_number_image(self):
        height = settings.PROFILE_IMAGE_HEIGHT_MIN
        width = settings.PROFILE_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{width}/{height}').content
        image = SimpleUploadedFile(
            name='test_profile',
            content_type='image/jpeg',
            content=image_content,
        )
        user = User.objects.create(
            username='user5',
            email='user5@domain.com',
            gender='m',
            birthday='2000-01-07',
            phone_number='+989123456789',
            image=image,
        )
        user.set_password('v,T7DzBqkhefcarJ')
        self.assertIsNotNone(User.objects.get(username='user5'))

    def test_create_ok_user_with_username_password_gender_birthday_phone_number_image_first_name(self):
        height = settings.PROFILE_IMAGE_HEIGHT_MIN
        width = settings.PROFILE_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{width}/{height}').content
        image = SimpleUploadedFile(
            name='test_profile',
            content_type='image/jpeg',
            content=image_content,
        )
        user = User.objects.create(
            username='user6',
            email='user6@domain.com',
            gender='m',
            birthday='2000-01-07',
            phone_number='+989123456789',
            image=image,
            first_name='user6_first_name'
        )
        user.set_password('v,T7DzBqkhefcarJ')
        self.assertIsNotNone(User.objects.get(username='user6'))

    def test_create_ok_user_with_username_password_gender_birthday_phone_number_image_first_name_last_name(self):
        height = settings.PROFILE_IMAGE_HEIGHT_MIN
        width = settings.PROFILE_IMAGE_WIDTH_MIN
        image_content = requests.get(f'https://picsum.photos/{width}/{height}').content
        image = SimpleUploadedFile(
            name='test_profile',
            content_type='image/jpeg',
            content=image_content,
        )
        user = User.objects.create(
            username='user7',
            email='user7@domain.com',
            gender='m',
            birthday='2000-01-07',
            phone_number='+989123456789',
            image=image,
            first_name='user7_first_name',
            last_name='user7_last_name',
        )
        user.set_password('v,T7DzBqkhefcarJ')
        self.assertIsNotNone(User.objects.get(username='user7'))

    def test_wrong_easy_password(self):
        user = User.objects.create(username='user8', email='user8@domain.com')
        with self.assertRaises(ValidationError):
            user.set_password('password')

    def test_wrong_less_length_password(self):
        user = User.objects.create(username='user9', email='user9@domain.com')
        with self.assertRaises(ValidationError):
            user.set_password('C3#Z')

    def test_wrong_all_numeric_length_password(self):
        user = User.objects.create(username='user9', email='user9@domain.com')
        with self.assertRaises(ValidationError):
            user.set_password('20661550698380342')

    def test_wrong_gender(self):
        with self.assertRaises(ValidationError):
            User.objects.create(username='user10', email='user10@domain.com', gender='x')

    def test_wrong_birthday(self):
        with self.assertRaises(ValidationError):
            User.objects.create(username='user11', email='user11@domain.com', birthday='2000-04-31')

    def test_wrong_phone_number_plus98(self):
        with self.assertRaises(ValidationError):
            User.objects.create(username='user10', email='user10@domain.com', phone_number='+98912345678')

    def test_wrong_phone_number_09(self):
        with self.assertRaises(ValidationError):
            User.objects.create(username='user10', email='user10@domain.com', phone_number='0912345678')

    def test_wrong_image(self):
        height = settings.PROFILE_IMAGE_HEIGHT_MAX * 2
        image_content = requests.get(f'https://picsum.photos/{height}').content
        image = SimpleUploadedFile(
            name='test_profile',
            content_type='image/jpeg',
            content=image_content,
        )
        with self.assertRaises(ValidationError):
            User.objects.create(username='user11', email='user11@domain.com', image=image, )

    def test_ok_delete_user(self):
        user = User.objects.create(username='user12', email='user12@domain.com')
        user.delete()
        self.assertIsNone(User.objects.filter(username='user12', ).first())

    def test_ok_save_user(self):
        user = User(username='user13', email='user13@domain.com')
        user.save()
        user.save()
        user.save()
        self.assertIsNotNone(User.objects.filter(username='user13', ).first())

    def test_ok_is_author_user_false(self):
        user = User(username='user14', email='user14@domain.com')
        user.save()
        self.assertFalse(user.is_author())

    def test_ok_is_author_user_true(self):
        user = User(username='user15', email='user15@domain.com')
        user.save()
        user.user_permissions.add(Permission.objects.get(codename='is_author'))
        user.save()
        self.assertTrue(user.is_author())

    def test_ok_is_activate_user_true(self):
        user = User(username='user17', email='user17@domain.com')
        user.save()
        self.assertTrue(user.is_active)

    def test_ok_is_activate_user_false(self):
        user = User(username='user18', email='user18@domain.com')
        user.is_active = False
        user.save()
        self.assertFalse(user.is_active)

    def test_ok_change_password(self):
        user = User.objects.create(username='user19', email='user19@domain.com')
        user.set_password('cPt}Y_bG{2Z(D)3#')
        user.set_password('7Yj`(6>^8KK.kZfb')
        hash_password = make_password('7Yj`(6>^8KK.kZfb')
        self.assertIsNotNone(hash_password, User.objects.get(username='user19').password)

    def test_wrong_change_password_empty_password(self):
        user = User.objects.create(username='user19', email='user19@domain.com')
        user.set_password('cPt}Y_bG{2Z(D)3#')
        with self.assertRaises(ValidationError):
            user.set_password('')

    def test_wrong_change_password_all_numeric(self):
        user = User.objects.create(username='user20', email='user20@domain.com')
        user.set_password('cPt}Y_bG{2Z(D)3#')
        with self.assertRaises(ValidationError):
            user.set_password('178326547324785634287')

    def test_wrong_change_password_easy(self):
        user = User.objects.create(username='user21', email='user21@domain.com')
        user.set_password('cPt}Y_bG{2Z(D)3#')
        with self.assertRaises(ValidationError):
            user.set_password('password')

    def test_ok_change_image(self):
        height = settings.PROFILE_IMAGE_HEIGHT_MIN
        image_content = requests.get(f'https://picsum.photos/{height}').content
        image = SimpleUploadedFile(
            name='test_profile',
            content_type='image/jpeg',
            content=image_content,
        )
        user = User.objects.create(username='user22', email='user22@domain.com', image=image, )
        image_content = requests.get(f'https://picsum.photos/{height}').content
        image = SimpleUploadedFile(
            name='test_profile_2',
            content_type='image/jpeg',
            content=image_content,
        )
        user.image = image
        user.save()
        saved_image_path = User.objects.get(username='user22').image.name
        saved_image_name = os.path.basename(saved_image_path)
        self.assertTrue(saved_image_name.startswith(image.name))

    def test_ok_change_username(self):
        user = User.objects.create(username='user23', email='user23@domain.com')
        user.set_password('+ZrUv{L]X9%557L`')
        user.username = 'user_tmp'
        user.save()
        self.assertIsNotNone(User.objects.get(username='user_tmp'))
        self.assertIsNone(User.objects.filter(username='user23').first())

    def test_wrong_change_username(self):
        user = User.objects.create(username='user24', email='user24@domain.com')
        User.objects.create(username='occupied', email='occupied@domain.com')
        user.set_password('Hf=D2j^MMRq"g+/9')
        user.username = 'occupied'
        with self.assertRaises(ValidationError):
            user.save()

    def test_ok_change_phone_number(self):
        user = User.objects.create(username='user24', email='user24@domain.com', phone_number='+989123456789')
        user.set_password('&sL~287.H=%n6mB5')
        user.set_phone_number('+989123456780')
        self.assertIsNotNone(User.objects.get(phone_number='+989123456780'))
        self.assertIsNone(User.objects.filter(phone_number='+989123456789').first())

    def test_wrong_change_phone_number(self):
        user = User.objects.create(username='user24', email='user24@domain.com', phone_number='+989123456789')
        user.set_password('A/?#+B?DNpNv9+TK')
        with self.assertRaises(ValidationError):
            user.set_phone_number('+98912345678')

    def test_wrong_change_phone_number_occupied(self):
        user = User.objects.create(username='user24', email='user24@domain.com', phone_number='+989123456789')
        User.objects.create(username='occupied', phone_number='+989123456781')
        user.set_password('$"DG(_Pyd8S{?57!')
        with self.assertRaises(ValidationError):
            user.set_phone_number('+989123456781')

    def test_ok_change_email(self):
        user = User.objects.create(username='user25', email='user25_1@domain.com', )
        user.email = 'user25_2@domain.com'
        user.save()
        self.assertIsNotNone(User.objects.get(email='user25_2@domain.com'))
        self.assertIsNone(User.objects.filter(email='user25_1@domain.com').first())

    def test_wrong_change_email_occupied(self):
        user = User.objects.create(username='user26', email='user26@domain.com', phone_number='+989123456789')
        User.objects.create(username='occupied', email='occupied@domain.com')
        user.email = 'occupied@domain.com'
        with self.assertRaises(ValidationError):
            user.save()
