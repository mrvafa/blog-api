from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestMakeUserAdmin(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='mrvafa', email='mrvafa@domain.com', is_superuser=True, is_staff=True)
        user.set_password('":"F$6x,XPL]ER=Q')
        user.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'mrvafa', 'password': '":"F$6x,XPL]ER=Q'})
        self.superuser_token = respond.json()['key']

        self.user_1 = User.objects.create(username='user1', email='user1@domain.com')

        self.user_2 = User.objects.create(username='user2', email='user2@domain.com')
        self.user_2.set_password('UM5/s*:Gf)gv`CAQ')
        self.user_2.is_staff = True
        self.user_2.save()

        respond = self.client.post(reverse('rest_login'), data={'username': 'user2', 'password': 'UM5/s*:Gf)gv`CAQ'})
        self.user_2_token = respond.json()['key']

        self.user_3 = User.objects.create(username='user3', email='user3@domain.com')

    def test_ok_make_user_staff(self):
        data = {'is_staff': True}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        user_id = User.objects.get(username='user1').id
        respond = self.client.patch(reverse('change_user_permissions', args=(user_id,)), data=data)
        self.assertEqual(200, respond.status_code)
        self.assertTrue(User.objects.get(username='user1').is_staff)

    def test_ok_make_staff_user(self):
        data = {'is_staff': False}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        user_id = User.objects.get(username='user2').id
        respond = self.client.patch(reverse('change_user_permissions', args=(user_id,)), data=data)
        self.assertEqual(200, respond.status_code)
        self.assertFalse(User.objects.get(username='user2').is_staff)

    def test_ok_make_all_permissions_to_false(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        user_id = User.objects.get(username='mrvafa').id
        data = {'is_active': False, 'is_staff': False, 'is_superuser': False}
        respond = self.client.patch(reverse('change_user_permissions', args=(user_id,)), data=data)
        self.assertEqual(200, respond.status_code)
        self.assertFalse(User.objects.get(username='mrvafa').is_staff)
        self.assertFalse(User.objects.get(username='mrvafa').is_active)
        self.assertFalse(User.objects.get(username='mrvafa').is_superuser)
