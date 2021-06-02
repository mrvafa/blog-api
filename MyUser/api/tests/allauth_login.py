from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestAllAuthLogin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = {
            'username': 'user1',
            'email': 'user1@domain.com',
            'password1': 'm2^CexxBmsNrBx\'+',
            'password2': 'm2^CexxBmsNrBx\'+'
        }
        self.user_2 = User.objects.create(username='user2', email='email2@domain.com')
        self.user_2.set_password('!jX+2#~:SvX@mMz:')
        self.user_2.save()
        self.user_3 = User.objects.create(username='user3', email='email3@domain.com')

    def test_ok_login(self):
        res = self.client.post(reverse('rest_login'), data={'username': 'user2', 'password': '!jX+2#~:SvX@mMz:'})
        self.assertEqual(200, res.status_code)

    def test_ok_get_profile(self):
        user_data = {'username': 'user2', 'password': '!jX+2#~:SvX@mMz:'}
        token = self.client.post(reverse('rest_login'), data=user_data).json()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token["key"]}')
        res = self.client.get(reverse('rest_user_details'))
        self.assertEqual(200, res.status_code)

    def test_ok_get_profile_check_details(self):
        user_data = {'username': 'user2', 'password': '!jX+2#~:SvX@mMz:'}
        token = self.client.post(reverse('rest_login'), data=user_data).json()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token["key"]}')
        res = self.client.get(reverse('rest_user_details'))
        result = res.json()
        self.assertEqual('', result['first_name'])
        self.assertEqual('', result['last_name'])
        self.assertEqual('user2', result['username'])
        self.assertFalse('password' in result)

    def test_edit_get_profile_first_name(self):
        user_data = {'username': 'user2', 'password': '!jX+2#~:SvX@mMz:'}
        token = self.client.post(reverse('rest_login'), data=user_data).json()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token["key"]}')
        res = self.client.put(reverse('rest_user_details'), data={'first_name': 'Ali', 'username': 'user2'})
        result = res.json()
        self.assertEqual('Ali', result['first_name'])
        self.assertEqual('', result['last_name'])
        self.assertEqual('user2', result['username'])

    def test_edit_get_profile_last_name(self):
        user_data = {'username': 'user2', 'password': '!jX+2#~:SvX@mMz:'}
        token = self.client.post(reverse('rest_login'), data=user_data).json()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token["key"]}')
        res = self.client.put(reverse('rest_user_details'), data={'last_name': 'last_name', 'username': 'user2'})
        result = res.json()
        self.assertEqual('', result['first_name'])
        self.assertEqual('last_name', result['last_name'])
        self.assertEqual('user2', result['username'])

    def test_check_editable_email(self):
        user_data = {'username': 'user2', 'password': '!jX+2#~:SvX@mMz:'}
        token = self.client.post(reverse('rest_login'), data=user_data).json()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token["key"]}')
        res = self.client.put(reverse('rest_user_details'), data={'email': 'user3@domain.com', 'username': 'user2'})
        result = res.json()
        self.assertEqual(User.objects.get(username='user2').email, result['email'])

    def test_check_change_username_taken(self):
        user_data = {'username': 'user2', 'password': '!jX+2#~:SvX@mMz:'}
        token = self.client.post(reverse('rest_login'), data=user_data).json()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token["key"]}')
        res = self.client.put(reverse('rest_user_details'), data={'username': 'user3'})
        self.assertEqual(400, res.status_code)
