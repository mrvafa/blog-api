from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestAllAuthRegister(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_1 = User.objects.create(username='user1', email='email1@domain.com')
        self.user_1.set_password('KtPKL3\\<!)\\5m`J>')
        self.user_1.save()
        self.user_1_token = self.client.post(
            reverse('rest_login'),
            data={'username': 'user1', 'password': 'KtPKL3\\<!)\\5m`J>'}
        ).json()['key']

        self.user_2 = User.objects.create(username='user2', email='email2@domain.com')
        self.user_2.set_password(';u4rQ@gRa+BfbpM~')
        self.user_2.save()
        self.user_2_token = self.client.post(
            reverse('rest_login'),
            data={'username': 'user2', 'password': ';u4rQ@gRa+BfbpM~'}
        ).json()['key']

    def test_ok_create_sms_code(self):
        data = {
            'phone_number': '09123456789',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        respond = self.client.post(reverse('send_sms'), data=data)
        self.assertEqual(201, respond.status_code)
