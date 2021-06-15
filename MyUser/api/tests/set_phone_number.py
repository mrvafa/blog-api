from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestListOfUsers(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create(username='user1', email='user1@domain.com')
        self.user_1.set_password(':-Z\\^&z{NXJ\';zq8u')
        self.user_1.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'user1', 'password': ':-Z\\^&z{NXJ\';zq8u'})
        self.user_1_token = respond.json()['key']

        self.user_2 = User.objects.create(username='user2', email='user2@domain.com')
        self.user_2.set_password('Uxm%Yr8cWveB]CL?')
        self.user_2.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'user2', 'password': 'Uxm%Yr8cWveB]CL?'})
        self.user_2_token = respond.json()['key']

    def test_ok_set_phone_number(self):
        data = {
            'phone_number': '09123456789',
            'code': '123',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        respond = self.client.put(reverse('set_phone_number_user'), data=data)
        self.assertEqual(200, respond.status_code)
        self.assertEqual('+989123456789', User.objects.first().phone_number)

    def test_wrong_set_phone_number_wrong_code(self):
        data = {
            'phone_number': '09123456789',
            'code': 'wrong-code',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        respond = self.client.put(reverse('set_phone_number_user'), data=data)
        self.assertEqual(400, respond.status_code)

    def test_wrong_set_phone_number_wrong_phone_number(self):
        data = {
            'phone_number': '0912345678',
            'code': 'wrong-code',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        respond = self.client.put(reverse('set_phone_number_user'), data=data)
        self.assertEqual(400, respond.status_code)

    def test_wrong_set_phone_number_no_phone_number(self):
        data = {
            'code': 'wrong-code',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        respond = self.client.put(reverse('set_phone_number_user'), data=data)
        self.assertEqual(400, respond.status_code)

    def test_wrong_set_phone_number_no_code(self):
        data = {
            'phone_number': '09123456789',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        respond = self.client.put(reverse('set_phone_number_user'), data=data)
        self.assertEqual(400, respond.status_code)

    def test_wrong_set_phone_number_phone_number_is_taken(self):
        data = {
            'phone_number': '09123456789',
            'code': '123',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        self.client.put(reverse('set_phone_number_user'), data=data)

        data = {
            'phone_number': '09123456789',
            'code': '123',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.put(reverse('set_phone_number_user'), data=data)
        self.assertEqual(400, respond.status_code)
