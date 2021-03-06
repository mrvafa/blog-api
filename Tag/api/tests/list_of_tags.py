from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from Tag.models import Tag


class TestListOfTags(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag_1 = Tag.objects.create(title='t1')
        self.tag_2 = Tag.objects.create(title='t2')
        self.tag_3 = Tag.objects.create(title='t3')

    def test_ok_list_of_tags(self):
        respond = self.client.get(reverse('tag_list'))
        self.assertEqual(200, respond.status_code)

    def test_ok_list_of_tags_check_ordering(self):
        respond = self.client.get(reverse('tag_list'))
        tags = respond.json()['results']
        self.assertEqual('t3', tags[0]['title'])
        self.assertEqual('t2', tags[1]['title'])
        self.assertEqual('t1', tags[2]['title'])

    def test_ok_search(self):
        respond = self.client.get(reverse('tag_list') + '?search=t1')
        tags = respond.json()['results']
        self.assertEqual(1, len(tags))
        self.assertEqual('t1', tags[0]['title'])

    def test_ok_ordering_title(self):
        respond = self.client.get(reverse('tag_list') + '?ordering=-title')
        tags = respond.json()['results']
        self.assertEqual('t3', tags[0]['title'])
