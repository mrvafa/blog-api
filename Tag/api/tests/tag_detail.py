from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from Tag.models import Tag


@override_settings(ACCOUNT_EMAIL_VERIFICATION='none')
class TestDetailOfTag(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag_1 = Tag.objects.create(title='t1', )
        self.tag_2 = Tag.objects.create(title='t2', )
        self.tag_3 = Tag.objects.create(title='t3', )

    def test_ok_detail_of_tag(self):
        respond = self.client.get(reverse('tag_detail', args=('t1',)))
        self.assertEqual(200, respond.status_code)
        self.assertEqual(self.tag_1.slug, respond.json()['slug'])

    def test_wrong_put_tag(self):
        respond = self.client.put(reverse('tag_detail', args=('t1',)))
        self.assertEqual(405, respond.status_code)
