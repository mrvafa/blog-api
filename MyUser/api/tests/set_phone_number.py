from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none', SMS_BACKEND='sms.backends.console.SmsBackend')
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

    @override_settings(SMS_CODE_FOR_TEST='123')
    def test_ok_set_phone_number(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        res = self.client.post(
            reverse('send_sms'),
            data={'phone_number': '09123456789'}
        )
        self.assertEqual(201, res.status_code)
        res = self.client.put(
            reverse('set_phone_number_user'),
            data={
                'phone_number': '09123456789',
                'code': '123'
            },
        )
        self.assertEqual(200, res.status_code)
        self.assertEqual('+989123456789', User.objects.get(username='user1').phone_number)

    @override_settings(SMS_CODE_FOR_TEST='123')
    def test_wrong_set_phone_number_wrong_code(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        res = self.client.post(
            reverse('send_sms'),
            data={'phone_number': '09123456789'}
        )
        self.assertEqual(201, res.status_code)
        res = self.client.put(
            reverse('set_phone_number_user'),
            data={
                'phone_number': '09123456789',
                'code': '1234'
            },
        )
        self.assertEqual(400, res.status_code)
        self.assertIsNone(User.objects.get(username='user1').phone_number)

    def test_wrong_set_phone_number_taken_phone_number(self):
        user = User.objects.create(email='user11@email.com', username='user11', )
        user.set_phone_number('+989123456789')

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        res = self.client.post(
            reverse('send_sms'),
            data={'phone_number': '09123456789'}
        )
        self.assertEqual(400, res.status_code)
        self.assertIsNone(User.objects.get(username='user1').phone_number)

    def test_wrong_set_phone_number_wrong_phone_number(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1_token}')
        res = self.client.post(
            reverse('send_sms'),
            data={'phone_number': '9123456789'}
        )
        self.assertEqual(400, res.status_code)
        self.assertIsNone(User.objects.get(username='user1').phone_number)
