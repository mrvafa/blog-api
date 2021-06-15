from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestListOfUsers(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create(username='user1', email='user1@domain.com')
        self.user_1.set_password(':YYYF!*j,PmsLc6,')

        self.user_2 = User.objects.create(username='user2', email='user2@domain.com')
        self.user_2.set_password('}\\sSJH)U@FzM:a7^')
        self.user_2.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'user2', 'password': '}\\sSJH)U@FzM:a7^'})
        self.user_2_token = respond.json()['key']

        self.user_3 = User.objects.create(username='user3', email='user3@domain.com')
        self.user_2.set_password('Kb[/;LmK#S"Kb8!w')

    def test_ok_get_edit_first_last_name(self):
        data = {
            'first_name': 'my first name',
            'last_name': 'my last name',

        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.get(reverse('edit_account'), data=data)
        first_name = respond.json()['first_name']
        last_name = respond.json()['last_name']
        self.assertEqual('', first_name)
        self.assertEqual('', last_name)

    def test_ok_put_edit_first_last_name(self):
        data = {
            'first_name': 'my first name',
            'last_name': 'my last name',

        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.patch(reverse('edit_account'), data=data)
        first_name = respond.json()['first_name']
        last_name = respond.json()['last_name']
        self.assertEqual('my first name', first_name)
        self.assertEqual('my last name', last_name)

    def test_wrong_put_edit_username_taken(self):
        data = {
            'username': 'user3',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.patch(reverse('edit_account'), data=data)
        self.assertEqual(400, respond.status_code)

    def test_wrong_put_edit_gender(self):
        data = {
            'gender': 'x',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.patch(reverse('edit_account'), data=data)
        self.assertEqual(400, respond.status_code)

    def test_ok_put_edit_birthday(self):
        data = {
            'birthday': '2000-09-10',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.patch(reverse('edit_account'), data=data)
        self.assertEqual(200, respond.status_code)

    def test_wrong_put_edit_birthday(self):
        data = {
            'birthday': '2000-04-31',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.patch(reverse('edit_account'), data=data)
        self.assertEqual(400, respond.status_code)

    def test_wrong_put_phone_number(self):
        data = {
            'phone_number': '+9891234567899',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.patch(reverse('edit_account'), data=data)
        self.assertEqual(200, respond.status_code)
        self.assertEqual('', respond.json()['phone_number'])

    def test_ok_put_edit_phone_number(self):
        data = {
            'phone_number': '+989123456789',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.patch(reverse('edit_account'), data=data)
        self.assertEqual(200, respond.status_code)
