from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestListOfUsers(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='mrvafa', email='mrvafa@domain.com', is_superuser=True, is_staff=True)
        user.set_password('5HvFn5-/D[c=`+j4')
        user.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'mrvafa', 'password': '5HvFn5-/D[c=`+j4'})
        self.superuser_token = respond.json()['key']

        self.user_1 = User.objects.create(username='user1', email='user1@domain.com')

        self.user_2 = User.objects.create(username='user2', email='user2@domain.com')
        self.user_2.set_password(')4NcM76Bc+dzVR>+')
        self.user_2.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'user2', 'password': ')4NcM76Bc+dzVR>+'})
        self.user_2_token = respond.json()['key']

        self.user_3 = User.objects.create(username='user3', email='user3@domain.com')

    def test_ok_detail_of_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        respond = self.client.get(reverse('user_detail'), pk=1)
        self.assertEqual(200, respond.status_code)

    def test_ok_detail_of_user_check_ordering(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        respond = self.client.get(reverse('user_detail', args=(1,)))
        user = respond.json()
        self.assertEqual('mrvafa', user['username'])

    def test_wrong_detail_of_user_no_token(self):
        respond = self.client.get(reverse('user_detail', args=(1,)))
        self.assertEqual(401, respond.status_code)

    def test_wrong_detail_of_user_non_superuser_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.get(reverse('user_detail', args=(3, )))
        self.assertEqual(403, respond.status_code)
