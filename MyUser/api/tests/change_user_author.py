from django.contrib.auth.models import Permission
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestMakeUserAuthor(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='mrvafa', email='mrvafa@domain.com', is_superuser=True, is_staff=True)
        user.set_password('jb3%Rd2B+{9)dVDv')
        user.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'mrvafa', 'password': 'jb3%Rd2B+{9)dVDv'})
        self.superuser_token = respond.json()['key']

        self.user_1 = User.objects.create(username='user1', email='user1@domain.com')

        self.user_2 = User.objects.create(username='user2', email='user2@domain.com')
        self.user_2.set_password('QW_f3-MVP\\jh7Z#r')
        self.user_2.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'user2', 'password': 'QW_f3-MVP\\jh7Z#r'})
        self.user_2_token = respond.json()['key']

        self.user_3 = User.objects.create(username='user3', email='user3@domain.com')
        author_permission = Permission.objects.get(codename='is_author')
        self.user_3.user_permissions.add(author_permission)

    def test_ok_change_user_author(self):
        data = {'is_author': True}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        user_id = User.objects.get(username='user1').id
        respond = self.client.put(reverse('change_user_author', args=(user_id,)), data=data)
        self.assertEqual(200, respond.status_code)
        self.assertTrue(User.objects.get(username='user1').is_author())

    def test_ok_make_author_user(self):
        data = {'is_author': False}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        user_id = User.objects.get(username='user3').id
        respond = self.client.put(reverse('change_user_author', args=(user_id,)), data=data)
        self.assertEqual(200, respond.status_code)
        self.assertFalse(User.objects.get(username='user3').is_author())

    def test_ok_empty_data_is_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        user_id = User.objects.get(username='user1').id
        respond = self.client.put(reverse('change_user_author', args=(user_id,)), data={})
        self.assertEqual(200, respond.status_code)
        self.assertFalse(User.objects.get(username='user1').is_author())
