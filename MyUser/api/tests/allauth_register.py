from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from MyUser.models import User


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestAllAuthRegister(TestCase):
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
        self.user_3 = User.objects.create(username='user3', email='email3@domain.com')

    def test_ok_create_user(self):
        res = self.client.post(reverse('rest_register'), data=self.user_1)
        self.assertEqual(201, res.status_code)

    def test_ok_create_user_exist_in_db(self):
        self.client.post(reverse('rest_register'), data=self.user_1)
        self.assertEqual(self.user_1['username'], User.objects.get(username='user1').username)
