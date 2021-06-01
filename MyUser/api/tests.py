from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestAllAuth(TestCase):
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

    def test_ok_create_user(self):
        res = self.client.post(reverse('rest_register'), data=self.user_1)
        self.assertEqual(201, res.status_code)

    def test_ok_create_user_exist_in_db(self):
        self.client.post(reverse('rest_register'), data=self.user_1)
        self.assertEqual(self.user_1['username'], User.objects.get(username='user1').username)

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
