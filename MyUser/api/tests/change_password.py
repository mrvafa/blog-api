from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestAllAuthChangePassword(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1_current_password = '74kCexbXjZ69FLBM'
        self.user_1_new_password = 'Cp5teB3rV4Q3u9GZ'
        self.user_1 = User.objects.create(username='user1', email='email1@domain.com')
        self.user_1.set_password(self.user_1_current_password)
        self.user_1.save()
        self.user_1_data = {'username': 'user1', 'password': f'{self.user_1_current_password}'}

    def test_wrong_change_password_no_password(self):
        token = self.client.post(reverse('rest_login'), data=self.user_1_data).json()['key']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        respond = self.client.patch(reverse('change_password'))
        self.assertEqual(400, respond.status_code)

    def test_wrong_change_password_one_password(self):
        token = self.client.post(reverse('rest_login'), data=self.user_1_data).json()['key']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        respond = self.client.patch(reverse('change_password'), data={'new_password1': self.user_1_new_password})
        self.assertEqual(400, respond.status_code)

    def test_ok_change_password(self):
        token = self.client.post(reverse('rest_login'), data=self.user_1_data).json()['key']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        respond = self.client.patch(
            reverse('change_password'),
            data={'new_password1': self.user_1_new_password, 'new_password2': self.user_1_new_password}
        )
        self.assertEqual(200, respond.status_code)

    def test_ok_change_password_changed(self):
        token = self.client.post(reverse('rest_login'), data=self.user_1_data).json()['key']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.client.patch(
            reverse('change_password'),
            data={'new_password1': self.user_1_new_password, 'new_password2': self.user_1_new_password}
        )
        self.assertTrue(User.objects.get(username='user1').check_password(self.user_1_new_password))

    def test_ok_change_password_login(self):
        token = self.client.post(reverse('rest_login'), data=self.user_1_data).json()['key']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.client.patch(
            reverse('change_password'),
            data={'new_password1': self.user_1_new_password, 'new_password2': self.user_1_new_password}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'')
        token = self.client.post(
            reverse('rest_login'),
            data={'username': 'user1', 'password': f'{self.user_1_new_password}'}
        ).json()['key']
        self.assertIsNotNone(token)

        respond = self.client.post(
            reverse('rest_login'),
            data={'username': 'user1', 'password': f'{self.user_1_current_password}'}
        )
        self.assertEqual(400, respond.status_code)

    def test_ok_change_password_check_different_tokens(self):
        old_token = self.client.post(reverse('rest_login'), data=self.user_1_data).json()['key']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {old_token}')
        respond = self.client.patch(
            reverse('change_password'),
            data={'new_password1': self.user_1_new_password, 'new_password2': self.user_1_new_password}
        )
        self.assertEqual(200, respond.status_code)
        self.client.credentials(HTTP_AUTHORIZATION=f'')
        new_token = self.client.post(
            reverse('rest_login'),
            data={'username': 'user1', 'password': f'{self.user_1_new_password}'}
        ).json()['key']

        self.assertNotEqual(old_token, new_token)
