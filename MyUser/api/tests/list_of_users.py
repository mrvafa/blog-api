from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestPrivateListOfUsers(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='mrvafa', email='mrvafa@domain.com', is_superuser=True, is_staff=True)
        user.set_password('k[25Fy;Yr,\\PBNg6')
        user.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'mrvafa', 'password': 'k[25Fy;Yr,\\PBNg6'})
        self.superuser_token = respond.json()['key']

        self.user_1 = User.objects.create(username='user1', email='user1@domain.com')

        self.user_2 = User.objects.create(username='user2', email='user2@domain.com')
        self.user_2.set_password('&m"4rc&\\B5)sV3n#')
        self.user_2.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'user2', 'password': '&m"4rc&\\B5)sV3n#'})
        self.user_2_token = respond.json()['key']

        self.user_3 = User.objects.create(username='user3', email='user3@domain.com')

    def test_ok_list_of_users(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        respond = self.client.get(reverse('private_user_list'))
        self.assertEqual(200, respond.status_code)

    def test_ok_list_of_users_check_ordering(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        respond = self.client.get(reverse('private_user_list'))
        users = respond.json()['results']
        self.assertEqual('user3', users[0]['username'])
        self.assertEqual('user2', users[1]['username'])
        self.assertEqual('user1', users[2]['username'])
        self.assertEqual('mrvafa', users[3]['username'])

    def test_wrong_list_of_users_no_token(self):
        respond = self.client.get(reverse('private_user_list'))
        self.assertEqual(401, respond.status_code)

    def test_wrong_list_of_users_non_superuser_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.get(reverse('private_user_list'))
        self.assertEqual(403, respond.status_code)
