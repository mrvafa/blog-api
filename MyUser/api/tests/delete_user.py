from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestDeleteUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='mrvafa', email='mrvafa@domain.com', is_superuser=True, is_staff=True)
        user.set_password(',/MebQ~Ezy43%&B(')
        user.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'mrvafa', 'password': ',/MebQ~Ezy43%&B('})
        self.superuser_token = respond.json()['key']

        self.user_1 = User.objects.create(username='user1', email='user1@domain.com')

        self.user_2 = User.objects.create(username='user2', email='user2@domain.com')
        self.user_2.set_password('7F]N#/$@C3kE;Uh7')
        self.user_2.save()
        respond = self.client.post(reverse('rest_login'), data={'username': 'user2', 'password': '7F]N#/$@C3kE;Uh7'})
        self.user_2_token = respond.json()['key']

        self.user_3 = User.objects.create(username='user3', email='user3@domain.com')

    def test_ok_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        respond = self.client.get(reverse('user_destroy', args=(2,)))
        self.assertEqual(200, respond.status_code)
        respond = self.client.delete(reverse('user_destroy', args=(2,)))
        self.assertEqual(204, respond.status_code)

    def test_ok_delete_user_check_db(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.superuser_token}')
        self.client.delete(reverse('user_destroy', args=(1,)))
        self.assertIsNone(User.objects.filter(username='mrvafa').first())

    def test_wrong_destroy_user_no_token(self):
        respond = self.client.delete(reverse('user_destroy', args=(1,)))
        self.assertEqual(401, respond.status_code)

    def test_wrong_destroy_user_non_superuser_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2_token}')
        respond = self.client.delete(reverse('user_destroy', args=(3,)))
        self.assertEqual(403, respond.status_code)
